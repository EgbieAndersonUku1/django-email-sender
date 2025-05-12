from __future__ import annotations

import json
import logging

from dataclasses import dataclass
from datetime import datetime
from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from enum import Enum
from logging import Logger, LoggerAdapter
from traceback import format_exc
from typing import Any, Callable, ClassVar, Dict, List, Optional, Set, Union


from django_email_sender.models import EmailBaseLog
from django_email_sender.email_sender_constants import EmailSenderConstants, LoggerType
from django_email_sender.email_sender import EmailSender
from django_email_sender.email_sender_payload import EmailMetaData, EmailPayload
from django_email_sender.translation import safe_set_language, translate_message
from django_email_sender.utils import mark_method_for_debugging
from django_email_sender.validation import (
    validate_custom_email_model,
    validate_custom_formatter,
    validate_method_signature,
)

from django_email_sender.messages import (
    AuditTrailMessages,
    ConfigMessages,
    DebugMessages,
    EmailLogSummary,
    EmailMessages,
    EmailStatus,
    EnvironmentSettings,
    FieldMessages,
    FieldSummaryLog,
    LoggerMessages,
    LogExecutionMessages,
    MethodConstants,
    RecipientMessages,
    TemplateMessages,
    TemplateResolutionMessages,
)

from django_email_sender.exceptions import (
    ContextIsNotADictionary,
    EmailSendError,
    EmailSenderBaseException,
    EmailTemplateNotFound,
    IncorrectEmailModelAddedError,
    IncorrectEmailSenderInstance,
    IncorrectLoggerLevelSettings,
    InvalidMetadata,
    InvalidPayload,
    LoggerTypeError,
    MissingFieldsInClass,
    LoggerBaseException,
)


# from django_email_sender.exceptions import LoggerBaseException, LoggerTypeError

from django_email_sender.utils import get_template_dirs
from django_email_sender.email_sender_constants import (
    EmailSenderConstants,
    get_email_sender_param_contract,
)

from django_email_sender.utils import get_html_preview, get_safe_text_preview
from django_email_sender.utils import measure_duration


dirs                = get_template_dirs()
TEMPLATES_DIR       = dirs["TEMPLATES_DIR"]
EMAIL_TEMPLATES_DIR = dirs["EMAIL_TEMPLATES_DIR"]

from typing import Callable, Optional, Any, Set, Dict, List
from logging import Logger


@dataclass(frozen=True)
class _EmailSenderLoggerKeys:
    """
    A data class that defines constant keys used for logging email sender operations.

    This class holds constant keys and a set of predefined logger levels.
    
    The class is frozen, meaning its attributes are immutable.

    Attributes:
        METHOD (str): The key used to represent the method name in logging.
        METHOD_PARAMS (str): The key used to represent method parameters in logging.
        TEMPLATE_FOLDER_KEY (str): The key used to represent the folder location 
                                    of the email templates in logging.
        LOGGER_LEVELS (ClassVar[Set[str]]): A class-level set of supported logger 
                                            levels, which includes 'error', 'debug', 
                                            'warning', and 'info'.
    """
    
    METHOD: str                       = "method"
    METHOD_PARAMS: str                = "params"
    TEMPLATE_FOLDER_KEY: str          = "folder"
    LOGGER_LEVELS: ClassVar[Set[str]] = {"error", "debug", "warning", "info"}



class EmailSenderLogger:
    """
    Handles structured email logging using a provided logger instance.

    NOTE: This class does not configure or modify the provided logger.
    It assumes the user has already set up logging handlers, formatters,
    encoding, and output destinations according to their environment.
    This design prevents interference with user-defined logging configurations.
    """

    def __init__(self) -> None:
        
        self._show_traceback_error: bool               = False
        self._method_tracing                           = False
        self._logger: Optional[Logger]                 = None
        self._logging_enabled: bool                    = False
        self._logger_levels: Set[str]                  = _EmailSenderLoggerKeys.LOGGER_LEVELS
        self._debug_verbose: bool                      = False
        self._is_config: bool                          = False
        self._current_log_level: str                   = None
        self._logger_started: bool                     = False
        self._email_sender: EmailSender                = None
        self._text_preview: str                        = None
        self._html_preview: str                        = None
        self._field_changes: Dict[str, Any]            = {}
        self._TEMPLATE_FOLDER_KEY: str                 = _EmailSenderLoggerKeys.TEMPLATE_FOLDER_KEY
        self._email_delivery_count: int                = 0
        self._is_delivery_successful: bool             = False
        self._enable_field_trace_logging: bool         = False
        self._fields: Set                              = set()  
        self._is_headers_set: bool                     = False
        self._is_context_set: bool                     = False
        self._exclude_fields: Optional[Set[str]]       = set()
        self._enable_exclusion_field_trace: bool       = False
        self._was_sent_successfully                    = False
        self._email_was_processed                      = None
        self._log_model                                = None
        self._meta_data: json                          = None
        self._custom_formatter: Optional[Callable[[str], str]] = None
        self._email_sender_paras: dict                 = get_email_sender_param_contract()
        self._save_errors_to_db                        = False
        self._to_db                                    = False
        self._fields_marked_for_reset                  = False
        self._email_payload                            = None
        self._methods_seen                             = []
        safe_set_language(self._logger)

    @classmethod
    def create(cls):
        """
        Class factory method to initialize the EmailSender for method chaining.

        Returns:
            EmailSenderLogger: A new instance of EmailSender.
        """
        return cls()

    def add_email_sender_instance(self, email_sender_instance: EmailSender) -> "EmailSenderLogger":
        """ 
        Adds an instance of the EmailSender class to the EmailSenderLogger. 
        This instance will be used to log emails and their outcomes.

        Args:
            email_sender_instance (EmailSender): An instance of EmailSender to log sent emails and their outcomes.

        Raises:
            IncorrectEmailSenderInstance: If the provided instance is not an instance of EmailSender.
            MissingFieldsInClass: If required fields or methods are missing in the class.

        Returns:
            Returns an EmailSenderLogger instance.
            
        Example Usage:

            from django_email_sender.email_sender import EmailSender
            from django_email_sender.email_logger import EmailSenderLogger
            
            # Create and add an EmailSender instance for logging
            email_logger = EmailSenderLogger.create().add_email_sender_instance(EmailSender())
            
            # Alternative: Use a class method to create the EmailSender instance
            email_logger = EmailSenderLogger.create().add_email_sender_instance(EmailSender.create())
        """
        
        self._is_email_sender_class_valid(email_sender_instance)
        
        self._email_sender = email_sender_instance.create()
        class_name         = email_sender_instance.__class__.__name__

        self._log_message(ConfigMessages.CONFIG_SETUP_SUCCESS, config_details=class_name)
    
        self._log_debug_trace_format()
        
        return self
    
    def _is_email_sender_class_valid(self, email_sender_instance: EmailSender):
        """
        Validates whether the provided EmailSender instance is valid. 
        If the instance is not valid, it raises relevant errors.

        Args:
            email_sender_instance (EmailSender): An instance of EmailSender to log sent emails and their outcomes.

        Raises:
            IncorrectEmailSenderInstance: If the provided instance is not an instance of EmailSender.
            MissingFieldsInClass: If required fields or methods are missing in the class.

        Returns:
            bool: Returns True if the EmailSender instance is valid; otherwise, it raises an exception.
        """
        self._log_debug_trace_format()
        EXPECTED_TYPE = "EmailSender instance"
        
        if not isinstance(email_sender_instance, EmailSender):
            
            error_msg = ConfigMessages.format_message(
                
                ConfigMessages.INCORRECT_CONFIG_TYPE,
                expected_type=EXPECTED_TYPE,
                actual_type=email_sender_instance,
            )
            
            # catch the error, pass it to the log_message, if there is a custom_formatter
            # it format the error message according to user design, and then re-raise it
            try:
                raise IncorrectEmailSenderInstance(ConfigMessages.format_message(error_msg))
            except IncorrectEmailSenderInstance as e:
                self._log_message(error_msg, exc=e)
                raise IncorrectEmailSenderInstance(ConfigMessages.format_message(error_msg))

        class_name = email_sender_instance.__class__.__name__

        self._log_debug_verbose( MethodConstants.format_message(MethodConstants.EVALUATING_FIELD_METHODS, class_name=class_name))
             
        is_fields_valid  = self._validate_email_sender_fields(email_sender_instance)
        is_methods_valid = self._validate_email_sender_public_methods(email_sender_instance)

        if is_fields_valid and is_methods_valid:
            return True
        
        self._log_message(MethodConstants.MISSING_FIELDS_ERROR, fields=is_fields_valid, methods=is_methods_valid)
        raise MissingFieldsInClass(message=MethodConstants.MISSING_CLASS_FIELDS, fields=is_fields_valid, methods=is_methods_valid)
       
    def _validate_email_sender_public_methods(self, email_sender_instance):
        """ 
        Validates whether the public methods in the EmailSender instance is valid.
        Returns True if valid
        
        """
        self._log_debug_trace_format()
        return self._validate_required_fields_in_email_sender(email_sender_instance, EmailSenderConstants.PublicMethods, validate_method=True)
    
    def _validate_email_sender_fields(self, email_sender_instance):
        """
        Validates whether the public fields in the EmailSender instance is valid.
        Returns True if valid,
        """
        self._log_debug_trace_format()
        return self._validate_required_fields_in_email_sender(email_sender_instance, EmailSenderConstants.Fields)
        
    def _validate_required_fields_in_email_sender(self, email_sender_instance, fields: Enum, validate_method: bool = False):
        """
        Validates whether the required fields or methods in the EmailSender class are present and correctly defined.

        This method checks whether each attribute (field or method) specified in the `fields` Enum exists in the 
        `email_sender_instance`. If `validate_method` is True, it will also verify that methods have the correct
        signatures, including expected parameters and types.

        Args:
            email_sender_instance: The instance of the EmailSender class to be validated.
            fields (Enum): An Enum containing the names of both fields and methods that need to be validated.
            validate_method (bool): If True, methods will be validated by checking their signatures. If False, only 
                                    the presence of fields will be validated.

        Returns:
            bool: True if all specified fields or methods are valid; False otherwise.
        """
        self._log_debug_trace_format()
        is_valid   = True
        class_name = email_sender_instance.__class__.__name__
        
         
        for field in fields:

            match validate_method:
            
                case True:
                    
                    field           = field.name
                    expected_params = self._email_sender_paras.get(field)
                    method_name     = expected_params.get(_EmailSenderLoggerKeys.METHOD)
                    params          = expected_params.get(_EmailSenderLoggerKeys.METHOD_PARAMS)

                    try:
                        has_field = validate_method_signature(obj=email_sender_instance, method_name=method_name, expected_params=params)
                        self._log_debug_verbose(MethodConstants.EVALUATING_FIELD_METHODS, field=field, class_name=class_name, has_field=has_field)
                        self._log_debug_verbose(MethodConstants.METHOD_PARAMS_CHECK, class_name=class_name, method=method_name, params=params)
                        
                    except ValueError as e:
                        error_msg = MethodConstants.EXCEPTION_ERRORS.format(method=field, field=expected_params)
                        self._log_debug_verbose(error_msg)
                        self._log_message(error_msg, exc=e)
                        has_field = None
                        
                    except AttributeError:
                        error_msg = MethodConstants.EXCEPTION_ERRORS.format(method=field, field=expected_params)
                        self._log_debug_verbose(error_msg)
                        self._log_message(error_msg, exc=e)
                        has_field = None
                        
                case _:
                    
                    field      = field.value
                    has_field  = hasattr(email_sender_instance, field)
                    self._log_debug_verbose(MethodConstants.METHOD_FIELD_SIGNATURE_CHECK, field=field, class_name=class_name, has_field=has_field)

            if has_field is None or not has_field:
                is_valid = False
        
        return is_valid

    def from_address(self, email: str) -> "EmailSenderLogger":
        """
        Set the sender's email address.

        Args:
            email (str): The sender's email address.

        Returns:()
           EmailSenderLogger: The current instance for chaining.
        """
        
        self._log_debug_trace_format()
        self._set_email_sender_field(field=EmailSenderConstants.Fields.FROM_EMAIL.value, value=email, expected_field_type=str)
        return self

    def to(self, recipient: str) -> "EmailSenderLogger":
        """
        Set the recipient(s) of the email.

        If a single email is provided as a string, it converts it into a list.
        Otherwise, it assumes a list of email addresses.

        Args:
            recipients (Union[str, List[str]]): A single email address or a list of email addresses.

        Returns:
           EmailSenderLogger: The current instance for chaining.
        """
        self._log_debug_trace_format()
        self._set_email_sender_field(field=EmailSenderConstants.Fields.TO_EMAIL.value, value=recipient, expected_field_type=str)
        return self

    def with_subject(self, subject: str) -> "EmailSenderLogger":
        """
        Set the subject of the email.

        Args:
            subject (str): The subject line.

        Returns:
           EmailSenderLogger: The current instance for chaining.
        """
        
        self._log_debug_trace_format()
        self._set_email_sender_field(field=EmailSenderConstants.Fields.SUBJECT.value, value=subject, expected_field_type=str)
        return self

    def with_context(self, context: Dict) -> "EmailSenderLogger":
        """
        Set the context dictionary for rendering templates.

        Args:
            context (Dict): Context variables for use in templates.

        Returns:
           EmailSenderLogger: The current instance for chaining.
        """
        self._log_debug_trace_format()
    
        is_set = self._process_and_log_dictionary_fields(
                        field=EmailSenderConstants.Fields.CONTEXT.value,
                        value=context,
                        expected_type=dict
        )
     
        if is_set:
            self._is_context_set = True
        return self

    def with_html_template(self, template_name: str, folder_name: str = None) -> "EmailSenderLogger":
        """
        Set the HTML template path.

        Args:
            template_name (str): The name of the plain text template file (e.g. 'welcome.html').
            folder_name (str, optional): The name of the subfolder inside the 'email_templates' directory
                                        where this template is located. If None, template is assumed to
                                        reside directly in the 'email_templates' folder.

        Returns:
           EmailSenderLogger: The current instance for chaining.
        """
        self._log_debug_trace_format()
      
        self._track_field_change("short_html_name", template_name)
        
        # Set the HTML template using the "with_html_template" method, which ensures the full template path is created
        # Unlike `set_email_sender_field`, this method not only sets the template name but also ensures that the
        # complete path is constructed, which is important for correctly locating the template.
        template_path   = self._email_sender.with_html_template(template_name, folder_name).html_template
           
        self._set_email_sender_field(
            
            field=EmailSenderConstants.Fields.HTML_TEMPLATE.value,
            value=template_path,
            expected_field_type=str,
            folder=folder_name,
            set_field_value=False # tells the method not to set to EmailSender since it has be set above
        )
        return self

    def with_text_template( self, template_name: str, folder_name: str = None) -> "EmailSenderLogger":
        """
        Set the plain text template path for the email.

        Args:
            template_name (str): The name of the plain text template file (e.g. 'welcome.txt').
            folder_name (str, optional): The name of the subfolder inside the 'email_templates' directory
                                        where this template is located. If None, template is assumed to
                                        reside directly in the 'email_templates' folder.

        Returns:
           EmailSenderLogger: The current instance for method chaining.
        """

        self._track_field_change("short_text_name", template_name)
        self._log_debug_trace_format()
        
        # Set the text template using the "with_html_template" method, which ensures the full template path is created
        # Unlike `set_email_sender_field`, this method not only sets the template name but also ensures that the
        # complete path is constructed, which is important for correctly locating the template.
        template_path  = self._email_sender.with_text_template(template_name, folder_name).text_template
     
        self._set_email_sender_field(
            field=EmailSenderConstants.Fields.TEXT_TEMPLATE.value,
            value=template_path,
            expected_field_type=str,
            folder=folder_name,
            set_field_value=False # tells the method not to set to EmailSender since it has be set above
        )
        return self

    def with_headers(self, headers: Dict) -> "EmailSenderLogger":
        """
        Set custom headers for the email.

        Args:
            headers (Optional[Dict], optional): A dictionary of headers to include in the email. Default is an empty dictionary.

        Raises:
            TypeError: If headers is not a dictionary.

        Returns:
            EmailSender: The current instance for chaining.
        """
        self._log_debug_trace_format()
        is_set =  self._process_and_log_dictionary_fields(
                        field=EmailSenderConstants.Fields.HEADERS.value,
                        value=headers,
                        expected_type=dict
        )
 
        if is_set:
            self._is_headers_set = True
        return self
    
    def _process_and_log_dictionary_fields(self, field: str, value: Dict , expected_type: Dict) -> bool:
        """
        Validates whether the provided value for a given field (e.g., 'headers' or 'context') is a dictionary.

        If the value is not a dictionary, logs the inconsistency and raises a ContextIsNotADictionary error.
        Returns True if the value is valid.

        Args:
            field (str): The name of the field being checked (e.g., 'headers' or 'context').
            value (Any): The value associated with the field.
            expected_type (type): The expected type for the field (typically Dict).

        Returns:
            bool: True if the value is a dictionary of the expected type; otherwise, an exception is raised.
        """
        self._log_debug_trace_format()
        try:
            self._set_email_sender_field(field=field, value=value, expected_field_type=expected_type)
        except ContextIsNotADictionary as e:
            self._log_incorrect_field_type(field, expected_field_type=Dict)
            
            raise ContextIsNotADictionary(message=str(e))
        return True

    def add_new_recipient(self, recipient: str):
        """
        Adds an additional email recipient to the list of recipients.

        This method ensures no duplicate recipients are added by storing
        them internally in a set.

        Args:
            recipient (str): The email address to add as a recipient.
        """

        self._log_debug_trace_format()
        
        self._email_sender.to(recipient)
        
        self._set_email_sender_field(
            
            field=EmailSenderConstants.Fields.LIST_OF_RECIPIENT.value,
            value=recipient,
            expected_field_type=str,
            add_multiple_recipients=True,
            set_field_value=False
            
        )
        return self
    
    
    def send(self, *args, **kwargs):
        """
        This method does not send email messages directly. Instead, it invokes the
        corresponding method on the EmailSender instance, passing in any arguments
        and logging the entire process.

        Args:
            *args: Positional arguments to pass to the EmailSender method.
            **kwargs: Keyword arguments to pass to the EmailSender method.
        """

        self._handle_auto_reset(**kwargs)
        recipients = list(self._email_sender.list_of_recipients)
        self._log_debug_trace_format()

        self._log_email_preparation_details(recipients)     
        self._load_template_preview_in_logger(preview_chars=100)

        
        try:
            # send the email, return the resp and the time it took
            email_resp, elasped         = measure_duration(self._email_sender.send, *args, **kwargs)
        
            emails_sent_count, is_sent  = email_resp
            timestamp                   = timezone.now()
            self._was_sent_successfully = is_sent
            self._email_was_processed   = True
            self._clear_methods_seen()
            
        except EmailSendError as e:
            self._create_meta_data(self._was_sent_successfully, timezone.now(), errors=True)
            self._log_and_raise_failed_email_delivery(error=e)
            return 
           
        except EmailTemplateNotFound as e:
            self._create_meta_data(self._was_sent_successfully, timezone.now(), errors=True)
            self._log_and_raise_failed_email_delivery(error=e)
            return
        
        except EmailSenderBaseException:
            missing_fields = EmailMessages.MISSING_EMAIL_FIELDS.format(subject=self._email_sender.subject,
                                                                       from_email=self._email_sender.from_email,
                                                                       to_email=self._email_sender.to_email,
                                                                       )
            self._log_and_raise_failed_email_delivery(error=missing_fields)
            
            raise EmailSenderBaseException(missing_fields)
        
        self._log_email_summary(time_taken=elasped, 
                                  status=is_sent, 
                                  additional_recipients=recipients, 
                                  emails_sent_count=emails_sent_count,
                                  timestamp=timestamp
                                  
                                  )
      
        
        if emails_sent_count > 0:
            self._is_delivery_successful = True
        
        if self._to_db:
            self._log_activity_to_db()
            
        self._create_meta_data(is_sent, timestamp)
        self._update_email_delivery_count(emails_sent_count)
        
        return 
    
    def _handle_auto_reset(self, **kwargs):
        """
        Checks for the 'auto_reset' parameter. If set, this method copies 
        essential data from the `EmailSender` instance into a separate payload 
        object before those fields are cleared.

        This ensures that `EmailLogger`, which relies on the `EmailSender` 
        fields for logging and metadata, can still access the necessary data 
        even after the original fields are reset.
        """
        if kwargs.get("auto_reset"):
            self._fields_marked_for_reset = True

            # Snapshot the current state of the email sender
            payload_data = {
                "from_email": self._email_sender.from_email,
                "to_email": self._email_sender.to_email,
                "subject": self._email_sender.subject,
                "body_html": self._email_sender.html_template,
                "body_text": self._email_sender.text_template,
                "context": self._email_sender.context,
                "headers": self._email_sender.headers,
            }

            # Use static data to construct the payload
            self._email_payload = EmailPayload(**payload_data)
        else:
            self._email_payload = self.payload

            
            
    def _log_email_preparation_details(self, recipients: list[str]) -> None:
        """
        Logs detailed information about the email setup before it is sent.

        This includes:
            - General logging markers
            - Number of recipients and their addresses
            - Sender and recipient email addresses
            - Subject line
            - Template paths for HTML and plain text versions
            - Email format

        Args:
            recipients (list[str]): A list of recipient email addresses to whom the email will be sent.
        """
        self._log_message(EmailLogSummary.SPACE)
        self._log_message(EmailMessages.START_EMAIL_SEND)
        self._log_message(EmailMessages.CHECK_FOR_LIST_OF_EMAIL_RECIPIENT)
        self._log_message(EmailMessages.FOUND_NUM_OF_RECIPIENT, num=len(recipients))
        self._log_message(EmailMessages.LIST_OF_RECIPIENTS, list_of_recipients=recipients)
        self._log_message(
            EmailMessages.SENDER_EMAIL,
            sender_email=self._email_sender.from_email,
            field=EmailSenderConstants.Fields.FROM_EMAIL.value
        )
        self._log_message(
            EmailMessages.SEND_TO_EMAIL,
            to_email=self._email_sender.to_email,
            field=EmailSenderConstants.Fields.FROM_EMAIL.value
        )
        self._log_message(
            EmailMessages.SUBJECT_LINE,
            subject=self._email_sender.subject,
            field=EmailSenderConstants.Fields.SUBJECT.value
        )
        self._log_message(
            EmailMessages.HTML_TEMPLATE_USED,
            html_template_path=self._email_sender.html_template,
            field=EmailSenderConstants.Fields.HTML_TEMPLATE.value
        )
        self._log_message(
            EmailMessages.TEXT_TEMPLATE_USED,
            text_template_path=self._email_sender.html_template,
            fields=EmailSenderConstants.Fields.TEXT_TEMPLATE.value
        )
        self._log_message(EmailMessages.EMAIL_FORMAT)

    def _log_and_raise_failed_email_delivery(self, error: str, exc: Exception = None) -> None:
        """
        Logs the provided error message and raises an EmailSendError with the same message.

        This method records the error in the log (including sender, recipient, and error details),
        adds additional debug information about template resolution, and then raises an EmailSendError.

        Args:
            error (str): The error message to log and raise.
            exc  (Exception): To be used if the user provides a custom formatter
        """
        self._log_debug_trace_format()
        self._log_message(EmailMessages.FAILED_TO_SEND_EMAIL.format(from_user=self._email_sender.from_email,
                                                                    to_user=self._email_sender.to_email, error=str(error)
                                                                    ), 
                                                                    LoggerType.ERROR,
                                                                    exc=exc
                
             )
        self._log_debug_info_for_template_resolution()
        raise EmailSendError(message=str(error))
    
    def _log_debug_info_for_template_resolution(self):
        """
        Logs detailed debug information related to the resolution of the email template.

        This includes:
        - The folder provided for template lookup.
        - The absolute path to the email templates directory.
        - The full path of the resolved HTML template.
        - A check to indicate whether the template file resides within the specified folder.
        """
        
        folder = folder=self._field_changes.get(self._TEMPLATE_FOLDER_KEY)
        path   = self._email_sender.html_template
        
        self._log_message(TemplateResolutionMessages.FOLDER_PROVIDED.format(folder=folder))
        self._log_message(TemplateResolutionMessages.EMAIL_DIRECTORY_PATH.format(directory=EMAIL_TEMPLATES_DIR))
        self._log_message(TemplateResolutionMessages.FULL_TEMPLATE_PATH.format(path=path))
        self._log_message(TemplateResolutionMessages.INSIDE_TEMPLATE_FOLDER_CHECK)

    def _get_environment(self):
        """
        Determines and returns the current environment (Development or Production).

        Since Django doesn't have a built-in explicit flag for 'production' or 'development',
        this method uses the DEBUG setting as a proxy. It assumes that when DEBUG is True,
        the environment is Development, and when DEBUG is False, it's Production.
        """ 
        self._log_debug_trace_format() 
        return EnvironmentSettings.DEVELOPMENT if settings.DEBUG else EnvironmentSettings.PRODUCTION

    def _set_email_sender_field(self, field: str, value: str, expected_field_type, set_field_value=True, *args, **kwargs) -> None:
        """Safely sets a field and logs the change."""
        
        current_value = getattr(self._email_sender, field, None)  # looks inside self._email_sender object class not the EmailSenderLogger
        
        if not value:
            self._log_field_not_set(field)
            return
        
        if not isinstance(value, expected_field_type):
            self._log_incorrect_field_type(value, expected_field_type)
            return
       
        if set_field_value:
             setattr(self._email_sender, field, value)  # sets the fields directly inside the EmailSender
        
        self._handle_multiple_recipient(field, value, kwargs)
      
        if self._should_skip_field_trace(field):
            return

        self._log_field_change(field_name=field, current_value=current_value, new_value=value)    
        self._resolve_template_folder(field, current_value, **kwargs)
        self._track_field_change(field=field, value=value)
    
    def _log_field_not_set(self, field: str) -> None:
        """
        Logs a warning message indicating that a specific field was accessed
        or referenced but no value has been set for it.

        Args:
            field (str): The name of the field that is not set.
        """
        self._log_debug_trace_format()
        self._log_message(
            FieldMessages.FIELD_NOT_SET.format(field=field),
            LoggerType.WARNING
        )


    def _log_incorrect_field_type(self, field: str, expected_field_type: Any):
        """
        Logs a message indicating that the type of a provided field value is incorrect,
        and follows up with a notice that no configuration action was taken as a result.

        Args:
            field (Any): The actual value or object whose type is being checked.
            expected_field_type (type (Any)): The expected type for the field.
        """
        self._log_debug_trace_format()
        self._log_message(FieldMessages.FIELD_TYPE_IS_INCORRECT.format(expected_type=expected_field_type, 
                                                                       received_type=type(field)))
        self._log_message(ConfigMessages.CONFIG_NO_ACTION_TAKEN)

        
    def _handle_multiple_recipient(self, field, value, kwargs):
        """
        Handles the addition of multiple recipients to the email sender's list.
        
        If the 'add_multiple_recipients' key is present in kwargs and the field is 'LIST_OF_RECIPIENT',
        it logs the addition of the recipient and adds them to the recipient list.
        
        Args:
            field (str): The field that triggered the action (e.g., 'LIST_OF_RECIPIENT').
            value (str): The value (email address) being added to the recipient list.
            kwargs (dict): Additional keyword arguments, including the flag to add multiple recipients.

        Returns:
            None
        """
        self._log_debug_trace_format()
        MULTIPLE_RECIPIENTS_KEY = "add_multiple_recipients"
        
        if kwargs.get(MULTIPLE_RECIPIENTS_KEY) and field == EmailSenderConstants.Fields.LIST_OF_RECIPIENT.value:
            self._log_message(RecipientMessages.RECIPIENT_ADDED_TO_LIST.format(recipient=value), LoggerType.DEBUG)
            self._email_sender.add_new_recipient(value)
    
    def _should_skip_field_trace(self, field: str) -> bool:
        """
        Determines whether the given field should be excluded from trace logging 
        based on the current trace and exclusion settings.

        Args:
            field (str): The field name to evaluate.

        Returns:
            bool: True if the field trace should be skipped, False otherwise.
        """
        self._log_debug_trace_format()
        
        if self._enable_field_trace_logging and not self._enable_exclusion_field_trace and field not in self._fields:
            self._log_debug_verbose(FieldSummaryLog.FIELDS_TO_SKIP, LoggerType.INFO, field=field)
            return True

        if self._enable_exclusion_field_trace and not self._enable_field_trace_logging and field in self._exclude_fields:
            self._log_debug_verbose(FieldSummaryLog.FIELDS_TO_SKIP, LoggerType.INFO, field=field)
            return True
        
        if self._enable_exclusion_field_trace and field not in self._exclude_fields:
            self._fields.add(field)
        

        return False

    def _resolve_template_folder(self, field: str, current_value: str, **kwargs: dict) -> None:
        """
        Resolves the template folder path based on keyword arguments.

        This method checks if a custom folder path has been provided in the kwargs.
        If not provided or set to None, it falls back to a default folder path and logs the appropriate message.

        Args:
            kwargs (dict): A dictionary of optional keyword arguments that may include 'template_folder'.

        Returns:
            str: The resolved template folder path to use.
        """

        folder = kwargs.get(self._TEMPLATE_FOLDER_KEY)
        self._log_debug_trace_format()

        if folder is None:

            self._track_field_change(field, current_value)

            self._log_debug_verbose(
                TemplateMessages.USING_DEFAULT_FOLDER.format(default_folder=EMAIL_TEMPLATES_DIR),
                LoggerType.INFO,
            )
            return

        self._log_message(
            TemplateMessages.format_message(TemplateMessages.OVERRIDE_FOLDER, folder_name=folder, default_folder=EMAIL_TEMPLATES_DIR)
        )

        self._log_field_change(field, current_value, folder)
        self._track_field_change(self._TEMPLATE_FOLDER_KEY, folder)

    def _log_field_change(self, field_name: str, current_value: str, new_value: str) -> None:
        """
        Logs a warning if a field is being changed from its current value.

        This is useful for auditing or debugging purposes, especially when you want
        to track updates to important attributes in the EmailSender class.

        Args:
            field_name (str): The name of the field being updated.
            current_value (Any): The existing value of the field.
            new_value (Any): The new value intended to replace the current one.
        """
        self._log_debug_trace_format()
        if current_value is None:
            
            self._log_message(FieldMessages.FIELD_SET.format(field=field_name, value=new_value))
            return
        
        if current_value != new_value:
            
            self._log_message(
                
                FieldMessages.FIELD_UPDATED.format(field=field_name, 
                                                   old_value=current_value, 
                                                   new_value=new_value
                                                   ), 
                logger_type=LoggerType.WARNING
            )
            
      
            self._log_debug_verbose(AuditTrailMessages.FIELD_CHANGED)
            self._log_debug_verbose(AuditTrailMessages.AUDIT_TRAIL_UPDATED)
            
            self._track_field_change(field=field_name, value=new_value)
        
            
            return

        self._log_message(FieldMessages.FIELD_SET.format(field=field_name, value=new_value), logger_type=LoggerType.DEBUG)

    def _track_field_change(self, field: str, value: Any) -> None:
        """
        Tracks a change to a field by saving the new value in a dictionary.

        Args:
            field (str): The name of the field being updated.
            value (Any): The new value to store for the field.
        """
        self._log_debug_trace_format()
        self._field_changes[field] = value
        self._log_debug_verbose(self._field_changes)
        self._log_debug_verbose(AuditTrailMessages.SHOW_AUDIT_TRAIL.format(audit_trail=self._get_field_audit()))

    def set_custom_formatter(self, custom_formatter: Optional[Union[Callable[[Exception, str], str], str]] = None) -> "EmailSenderLogger":
        """
        Sets a custom formatter for log messages.

        This allows users to define their own formatting logic for how exceptions and log messages are rendered.
        This can be as simple or as advance as the user needs it to be.  If no custom formatter is provided, the
        default Python logger formatting will be used.

        Args:
            custom_formatter (Optional[Union[Callable[[Exception, str], str], str]]):
                A function or string that defines the custom formatting logic.

        Returns:
            EmailSenderLogger: The current instance for method chaining.

        Example Usage:

        import logging
        from traceback import format_exception
        from my_email_module import EmailSenderLogger, LoggerType

        # Optional: Define a custom formatter function
        def my_custom_formatter(exc: Exception, msg: str) -> str:
            trace = ''.join(format_exception(type(exc), exc, exc.__traceback__))
            return f"[Custom Formatter] {msg}\nTraceback:\n{trace}"

        """
        self._log_debug_trace_format()
        if custom_formatter is not None:
            self._custom_formatter = validate_custom_formatter(custom_formatter)
        return self

    def set_traceback(self, show_traceback: bool = False, method_tracing: bool = False) -> "EmailSenderLogger":
        """
        Adds a full traceback to the log message when set to True. This will include detailed
        information about the error, including the point where it occurred. It will also show
        exactly which methods were called during your email building process, `set_traceback()` is your friend. 
        It provides a step-by-step breakdown of the chained method calls that lead up to sending an email when
        the method_tracing is set to True.

        Args:
            show_traceback (bool): A flag that determines whether a traceback should be 
                                included in the log message. Defaults to False.
            method_tracing (bool): shows the call between the methods

        Returns:
            EmailSenderLogger: The current instance of EmailSenderLogger, allowing for method chaining.
        """
        self._show_traceback_error = show_traceback
        self._method_tracing       = method_tracing
        return self

    def config_logger(self, logger: Logger, log_level: LoggerType | None = None) -> "EmailSenderLogger":
        """
        Configures the logger and sets the logging level.

        This method attaches a logger instance and defines the minimum level of messages
        that should be captured. The logger must be fully set up before being passed in.

        Supported log levels:
            DEBUG   - Captures all messages.
            INFO    - Captures INFO, WARNING, and ERROR messages.
            WARNING - Captures WARNING and ERROR messages.
            ERROR   - Captures only ERROR messages.

        Args:
            logger (Logger): A preconfigured logger instance.
            log_level (LoggerType | str | None): The minimum severity level for messages to be logged.
                                                If omitted, logging will be disabled even if a logger is set.
        """
      
        if self._is_config:
            
            self._log_debug_verbose(LoggerMessages.LOGGER_ALREADY_INITIALISED_WARNING, level=self._current_log_level)
            self._log_debug_verbose(ConfigMessages.CONFIG_NO_ACTION_TAKEN, LoggerType.DEBUG)
            return self

        self._is_logger_valid(logger)
        
        self._logger = LoggerAdapter(logger, {"component": self.__class__.__name__})
        self._is_config = True

        if self._set_level(log_level):

            self._log_debug_trace_format()

            self._log_message(LoggerMessages.CONFIG_LOG_LEVEL_SET)
            self._log_message(ConfigMessages.CONFIG_SETUP_SUCCESS, config_details=self._logger)
            safe_set_language(self._logger)
         
        return self

    def _is_logger_valid(self, logger: Logger) -> None:
        """
        Validates whether the provided logger is of a supported type.

        This method ensures:
            - The logger is not None.
            - The logger is an instance of either `Logger` or `LoggerAdapter`.

        Args:
            logger (Logger): The logger instance to validate.

        Raises:
            LoggerTypeError: If the logger is missing or not of a valid type.

        Returns:
            None
        """
        self._log_debug_trace_format()
        
        if not logger or logger is None:
            self._log_message(LoggerMessages.MISSING_LOGTYPE, LoggerType.ERROR)
            raise LoggerTypeError(LoggerMessages.MISSING_LOGTYPE)
            
        if logger:
            if not isinstance(logger, (Logger, LoggerAdapter)):
                self._log_message(LoggerMessages.INCORRECT_LOGTYPE, LoggerType.ERROR)
                raise LoggerTypeError(LoggerMessages.INCORRECT_LOGTYPE, logger_type=type(logger))
        return self

    def _set_level(self, logger_level: str) -> Optional[bool | None]:
        """
        Sets the user's logger level for logging. Raises an error if the 
        logger level is not one of the following levels 'error', 'warning', 'debug' or 'info'.
        
        Args:
            - logger_level (str) : The logger level that will be set to the user's logger
            
        Raises IncorrectLoggerLevelSettings:
            - Raises an error if the logger setting is not 'error', 'warning', 'debug' or 'info
            
        Returns:
            Returns the value None if there is no logger to set, and a bool value of 'True' if the logger has
            successfully been set.
        
        Note:
            The user must pass in a configured logger through the method '.config_logger' otherwise a
            value of None will be returned since there is no logger to actually set.
        """
        self._log_debug_trace_format()
        if logger_level is None:
            return None

        self._validate_logger_level(logger_level)
        
        logger_level = logger_level.upper()
        is_set = False
        
        if self._logger:

            self._current_log_level = logger_level
            self._logger.setLevel(logger_level)
            self._set_all_loggers(logger_level)
            is_set = True
            self._log_message(LoggerMessages.CONFIG_LOG_LEVEL_SET, level=logger_level)
        else:
            self._log_message(LoggerMessages.CONFIG_LOG_LEVEL_NOT_SET, level=logger_level)
        return is_set

    def _validate_logger_level(self, logger_level):
        """
        Validates that the provided logger level is correct.
        Logs an appropriate message if the logger level is invalid or not a string.
        
        Args:
            logger_level: The logger level to be validated.
            
        Raises:
            IncorrectLoggerLevelSettings: If the logger level is invalid or incorrectly typed.
        """
        valid   = True
        message = None
        self._log_debug_trace_format()
        
        if not isinstance(logger_level, str):
            
            message = ConfigMessages.INCORRECT_CONFIG_TYPE.format(expected_type="str", actual_type=type(logger_level))
            valid   = False
            self._log_message(message, LoggerType.DEBUG)
           
        try:
            if logger_level not in self._logger_levels:
                
                message = LoggerMessages.CONFIG_LOG_LEVEL_NOT_SET.format(level=logger_level)
                valid   = False
                self._log_message(message, LoggerType.DEBUG)
        except TypeError as e:
            raise LoggerBaseException(LoggerMessages.LOG_LEVEL_INCORRECT_TYPE, level=str(e))
                      
        if not valid:
            raise IncorrectLoggerLevelSettings(message)

    def _create_meta_data(self, is_sent: bool, timestamp: datetime, errors: str = None) -> None:
        """
        Creates the necessary meta data for a sent email. The metadata is created regardess
        of whether the email was successfully delivered. 
        
        The metadata includes the following: 
            - sender
            - recipient
            - status (whether it was sent or not)
            - timestamp (The date it was sent)
            - errors
        
        Args:
            - is_sent (bool): A boolean value that determines if an email was sent or not.
                            True means the email was not sent and False means it was
            
            - timestamp (datetime): The timestamp of when the email was sent.
           - errors (Any): Any errors that occurred when the email was sent 
        
        Raises InvalidMetadata:
            - Raises an InvalidMetadata error if the method fail to create the metadata
        
        """
        self._log_debug_trace_format()
        status = EmailStatus.SENT if is_sent else EmailStatus.NOT_SENT
        
        if not isinstance(timestamp, datetime):
            timestamp = timezone.now().isoformat()
        else:
            timestamp = timestamp.isoformat()
        
        if self._fields_marked_for_reset:
             meta_data = EmailMetaData(to_email=self._email_payload.to_email,
                                  subject=self._email_payload.subject,
                                  status=status,
                                  timestamp=timestamp,
                                  errors=errors
                                  )
        else:
            meta_data = EmailMetaData(to_email=self._email_sender.to_email,
                                    subject=self._email_sender.subject,
                                    status=status,
                                    timestamp=timestamp,
                                    errors=errors
                                    )
        
        is_valid = meta_data.is_valid()
        
        if not is_valid:
            raise InvalidMetadata(EmailMessages.ERROR_OCCURED)
        self._meta_data = meta_data.to_json()
            
    
    def add_log_model(self, log_model: EmailBaseLog) -> "EmailSenderLogger":
        """
        Registers a custom log model with the EmailSenderLogger to enable 
        database logging of sent emails via the `._log_activity_to_db()` method.
        
        The method `enable_email_meta_data_save` must be set for any data
        to be save to database.

        The custom model must be a class (not an instance) that inherits from 
        the abstract base model `EmailBaseLog`. This allows you to define any 
        additional fields or methods you want for tracking sent emails.

        Notes:
            1. Emails are logged to the database regardless of whether delivery 
            was successful, unless an exception occurs during logging.
            2. The argument must be a class (e.g., `CustomLogModel`), not an 
            instance (e.g., `CustomLogModel()`).

        Args:
            log_model (class): A class inheriting from `EmailBaseLog` to be 
            used for logging email activity.

        Raises:
            IncorrectEmailModelAddedError: 
                - If the model does not inherit from `EmailBaseLog`
                - If an instance is passed instead of a class

        Example:
            # models.py
            class CustomLogModel(EmailBaseLog):
                pass

            # views.py
            from django_email_sender.email_logger import EmailSenderLogger
            from your_app.models import CustomLogModel

            EmailSenderLogger.create().add_log_model(CustomLogModel)
        """
        self._log_debug_trace_format()
        try:
            validate_custom_email_model(log_model, EmailBaseLog)
        except TypeError as e:
            
            error_msg = IncorrectEmailModelAddedError(message=str(e))
            self._log_message(error_msg, exc=e)
            raise error_msg
        
        except Exception as e:
            error_msg = IncorrectEmailModelAddedError(message=str(e))
            self._log_message(error_msg, exc=e)
            raise error_msg
                  
        self._log_model = log_model
        return self
    
    def to_debug(self) -> "EmailSenderLogger":
        """
        Sets the debug to warning. Note the logger must be provide or nothing wil be set.
        """
        self._log_debug_trace_format()
        self._log_level_update_attempt(LoggerType.DEBUG)
        return self

    def to_info(self) -> "EmailSenderLogger":
        """
        Sets the logger to info. Note the logger must be provide or nothing wil be set.
        """
        self._log_debug_trace_format()
        self._log_level_update_attempt(LoggerType.INFO)
        return self

    def to_warning(self) -> "EmailSenderLogger":
        """
        Sets the logger to warning. Note the logger must be provide or nothing wil be set.
        """
        self._log_debug_trace_format()
        self._log_level_update_attempt(LoggerType.WARNING)
        return self

    def to_error(self) -> "EmailSenderLogger":
        """
        Sets the logger to error. Note the logger must be provide or nothing wil be set.
        """
        self._log_debug_trace_format()
        self._log_level_update_attempt(LoggerType.WARNING)
        return self
    
    def _log_level_update_attempt(self, level):
        """
        Logs the intent to update the logging level, attempts to update it,
        and logs the result of the update.

        This method is used internally to centralise the logic for 
        changing the logging level and recording that action.

        Args:
            level (str): The desired log level (e.g., 'DEBUG', 'INFO').

        Returns:
            self: Returns the logger instance to allow method chaining.
        """
        self._log_debug_trace_format()
        self._log_debug_verbose(LoggerMessages.LEVEL_REQUEST, level=level)
        is_set = self._set_level(level)
        
        if is_set:
            self._log_message(LoggerMessages.CONFIG_LOG_LEVEL_SET, level=level)
        else:
            self._log_message(LoggerMessages.CONFIG_LOG_LEVEL_NOT_SET, level=level)
        return self

    def _set_all_loggers(self, logger_level):
        """
        Logs the intent to update the logging level, attempts to update it,
        and logs the result of the update.

        This method is used internally to centralise the logic for 
        changing the logging level and recording that action.

        Args:
            level (str): The desired log level (e.g., 'DEBUG', 'INFO').

        Returns:
            self: Returns the logger instance to allow method chaining.
        """
        self._log_debug_trace_format()
        
        if logger_level not in self._logger_levels:
            self._log_message(LoggerMessages.CONFIG_LOG_LEVEL_NOT_SET, level=logger_level)
            self._log_message(LoggerMessages.NO_ACTION_TAKEN)
            return None

        for index, handler in enumerate(self._logger.handlers[:]):
            if isinstance(handler, logging.StreamHandler):
                self._logger.removeHandler(handler)
                self._log_debug_verbose("[Removed] Console handler {index}", LoggerType.INFO, index=index+ 1)
            else:
                handler.setLevel(logger_level)
                self._log_debug_verbose("[Setting] Handler {index}", LoggerType.INFO, index=index + 1)
                self._log_message(LoggerMessages.SET_LOG_LEVEL_FOR_HANDLERS_MSG, handler=handler, level=logger_level)

    def enable_verbose(self):
        """
        Enables verbose debugging output for the current instance.

        Sets the internal `_debug_verbose` flag to `True`, which can be used 
        by other methods to conditionally output detailed debug information.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        self._debug_verbose = True
        return self


    def disable_verbose(self):
        """
        Disable verbose debugging output for the current instance.

        Sets the internal `_debug_verbose` flag to `False`, which tells
        other methods not to log.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        self._debug_verbose = False
        return self

    def start_logging_session(self):
        """
        Starts a new logging session for the current instance.

        Sets internal flags `_logger_started` and `_logging_enabled` to `True`, 
        indicating that logging is active and initialized.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        self._logger_started  = True
        self._logging_enabled = True
        return self

    def stop_logging_session(self):
        """
        Terminates the current logging session for the instance.

        Disables logging by setting the internal flags `_logging_enabled` and 
        `_logger_started` to `False`. This terminates the logger and indication
        that no further logs should be emitted until '.start_logging_session()' is
        called again. 

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        self._logging_enabled = False
        self._logger_started = False
        return self

    def pause_logging(self) -> "EmailSenderLogger":
        """
        Pauses the current logging session without terminating the logger instance.

        Temporarily disables logging by setting the internal `_logging_enabled` flag 
        to `False`. Logging can be resumed later by calling `resume_logging()`.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        self._logging_enabled = False
        return self

    def resume_logging(self):
        """
        Resumes a previously paused logging session.

        Re-enables logging by setting the internal `_logging_enabled` flag 
        to `True`, allowing logs to be emitted again.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        self._logging_enabled = True
        return self

    @property
    def is_email_sent(self) -> bool:
        """
        Indicates whether the email was successfully delivered.

        Returns:
            bool: True if the email delivery was successful, False otherwise.
        """
        self._log_debug_trace_format()
        return self._is_delivery_successful
    
    @property
    def email_delivery_count(self):
        """
        Returns the number of email delivery attempts made by the instance.

        Returns:
            int: The count of email delivery attempts.
        """
        self._log_debug_trace_format()
        return self._email_delivery_count

    def clear_from_email(self):
        """
        Clears the sender email field and logs the action.

        Resets the 'from' email address in the internal email sender object, 
        and logs a message indicating that the field has been cleared.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        email = EmailSenderConstants.Fields.FROM_EMAIL.value
        self._email_sender.clear_from_email()
        self._log_field_cleared_message(email, self._email_sender.from_email)
        return self

    def clear_to_email(self):
        """
        Clears the recipient email field and logs the action.

        Resets the 'to' email address in the internal email sender object, 
        and logs a message indicating that the recipient field has been cleared.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        recipient = EmailSenderConstants.Fields.TO_EMAIL.value
        self._email_sender.clear_to_email()
        self._log_field_cleared_message(recipient, self._email_sender.to_email)
        return self

    def clear_subject(self):
        """
        Clears the subject field of the email and logs the action.

        Resets the subject line in the internal email sender object,
        and logs a message indicating that the subject field has been cleared.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        subject = EmailSenderConstants.Fields.SUBJECT.value
        self._email_sender.clear_subject()
        self._log_field_cleared_message(subject, self._email_sender.subject)
        return self

    def clear_context(self):
        """
        Clears the context field of the email and logs the action.

        Resets the context data used for rendering the email (e.g., in templates)
        in the internal email sender object, and logs that the context has been cleared.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        context = EmailSenderConstants.Fields.CONTEXT.value
        self._email_sender.clear_context()
        self._log_field_cleared_message(context, value=self._email_sender.context)
        return self

    def clear_text_template(self):
        """
        Clears the text template path used for rendering plain text emails and logs the action.

        Removes the text template reference from the internal email sender object,
        and logs a message indicating that the text template field has been cleared.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        text_template = EmailSenderConstants.Fields.TEXT_TEMPLATE.value
        self._email_sender.clear_text_template()
        self._log_field_cleared_message(text_template, value=self._email_sender.text_template)
        return self

    def clear_html_template(self):
        """
        Clears the HTML template path used for rendering HTML emails and logs the action.

        Removes the HTML template reference from the internal email sender object,
        and logs a message indicating that the HTML template field has been cleared.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        html_template = EmailSenderConstants.Fields.HTML_TEMPLATE.value
        self._email_sender.clear_html_template()
        self._log_field_cleared_message(html_template, value=self._email_sender.html_template)
        return self
    
    def clear_all_fields(self):
        """
        Clears all email fields and logs the action.

        Resets all relevant fields (e.g., sender, recipient, subject, context, etc.)
        in the internal email sender object, and logs a message indicating that
        all fields have been cleared.

        Returns:
            self: The current instance, allowing for method chaining.
        """
        self._log_debug_trace_format()
        
        ALL_FIELDS = _("All fields")
        self._email_sender.clear_all_fields()
        
        self._log_field_cleared_message(ALL_FIELDS, None)
        return self

    def _update_email_delivery_count(self, email_delivery_count: int) -> None:
        """
        Updates the email delivery count.

        Validates that the provided `email_delivery_count` is an integer and 
        greater than zero. If the validation passes, the count is added to 
        the existing email delivery count.

        Args:
            email_delivery_count (int): The number of email deliveries to add 
            to the current delivery count.

        Raises:
            TypeError: If `email_delivery_count` is not an integer.

        Returns:
            None
        """
        self._log_debug_trace_format()
        
        if not isinstance(email_delivery_count, int):
            raise TypeError(translate_message("Email delivery count must be an int. Got type {type_received}", 
                                            type_received=type(email_delivery_count))
                            )
        if email_delivery_count > 0:
            self._email_delivery_count += email_delivery_count

    def _log_field_cleared_message(self, field_name: str, value: str):
        """
        Logs a message indicating that a specific field has been cleared.

        Args:
            field_name (str): The name of the field that was cleared.
            value (str): The value of the field before it was cleared.

        Returns:
            None
        """
        self._log_debug_trace_format()
        self._log_debug_verbose(FieldMessages.FIELD_CLEARING_REQUEST, field=field_name) 
        self._log_message(FieldMessages.FIELD_HAS_BEEN_CLEARED, field=field_name, value=value)

    def _log_debug_trace_format(self, depth_trace=2):
        """
        Whenever it is called by other method logs a debug trace message with 
        information about the calling method and its call stack.

        This method logs information about the current method's execution, including the method name,
        class name, and line number, while also including a configurable depth trace level. If logging 
        is also enabled and the logger instance is available, it logs detailed debug information.

        Args:
            depth_trace (int, optional): The depth level of the trace. Defaults to 2.
                This controls how much of the call stack is traced.

        Raises:
            TypeError: If `depth_trace` is not an integer.

        Returns:
            None
        """
        if self._logger is None:
            return

        if not self._logging_enabled:
            self._log_debug_verbose(LoggerMessages.NOT_ENABLED)
            return

        if not isinstance(depth_trace, int):
            raise TypeError("Depth trace must be an integer")

        debug_info = mark_method_for_debugging(depth=depth_trace)

        if debug_info and self._debug_verbose:
            self._log_message(
                DebugMessages.format_message(
                    DebugMessages.format_message(
                        DebugMessages.VERBOSE_TRACE_ENTERED, depth_level=depth_trace
                    )
                )
            )
            self._log_message(
                DebugMessages.VERBOSE_TRACE,
                LoggerType.DEBUG,
                current_method=debug_info.CURRENT_METHOD,
                class_name=debug_info.CLASS_NAME,
                line_number=debug_info.LINE_NUMBER,
            )
            
        
            self._trace_method_call(debug_info.CLASS_NAME, debug_info.CURRENT_METHOD)

    def _trace_method_call(self, class_name, method_name):
        """
        Records and logs a method call in the current execution chain.

        This method is used to trace which methods have been invoked during
        the lifecycle of the EmailSenderLogger instance. It appends the method
        signature to an internal list if method tracing is enabled, and logs
        the resulting method chain for debugging purposes.

        :param class_name: Name of the class where the method is defined.
        :type class_name: str
        :param method_name: Name of the method being called.
        :type method_name: str
        """
        if not self._method_tracing:
            return
        
        signature = f"{class_name}.{method_name}()"
        if signature not in self._methods_seen:
            self._methods_seen.append(signature)
        
            
        method_trace = " --> ".join(self._methods_seen)
        self._log_debug_verbose(DebugMessages.METHOD_CHAIN_TRACE, LoggerType.DEBUG,  method_trace=method_trace)

    def return_successful_payload(self) -> Optional[dict]:
        """
        Returns the email payload for logging, but only if the email was successfully processed.

        This method should be called after the email has been sent. If the email was processed 
        successfully, it returns the full payload for logging. If the email hasn't been sent yet, 
        failed to send, or if the sender instance is missing, it returns False.

        Returns:
            dict | bool: The full email payload as a dictionary if the send attempt was successful,
                        otherwise None.
        """
        self._log_debug_trace_format()
        if self._email_sender and self._was_sent_successfully:
            return self.payload
        return None
    
    def enable_email_meta_data_save(self, save_to_db=True) -> "EmailSenderLogger":
        """
        Sets a flag to enable or disable saving email metadata to the database.
        This must be set before the 'send' method is called.
        
        Default: True
        """
        self._log_debug_trace_format()
        self._to_db = save_to_db
        return self

    def _log_activity_to_db(self) -> "EmailSenderLogger":
        """
        Logs the email activity to the database if the email has been processed 
        (whether it succeeded or failed). Returns self to allow method chaining.
        
        This must be called after the 'send' method to ensure that is logged to db.
        
        """
        # Only log to the database if the email was processed (sent, regardless of success or failure)
        
        self._log_debug_trace_format()
        
        is_valid = all([self._email_sender, self._log_model, self._to_db, self._email_was_processed])
        
        if is_valid:

            self._log_message(EmailMessages.START_DB_SAVE)
            is_saved_to_db = self._log_to_db()

            if is_saved_to_db:
                
                self._log_message(
                    EmailMessages.EMAIL_SAVED_TO_DB,
                    from_email=self._email_sender.from_email,
                    to_email=self._email_sender.to_email,
                    subject=self._email_sender.subject,
                    body_summary=self._text_preview
                )
        else:
            email_sender_class_name  = self._email_sender.__class__.__name__
            log_name_class           = self._log_model.__class__.__name__
            is_email_processed       = self._email_was_processed
            
            self._log_message(EmailMessages.FAILED_TO_START_DB_SAVE, class_name=email_sender_class_name,
                              log_model=log_name_class,
                              processed=is_email_processed
                              )
        return self
    
    @property
    def email_meta_data(self) -> json:
        """
        Returns the metadata related to the email, if available.

        Retrieves the metadata associated with the email from the internal
        email sender object. If no email sender is present, it returns an empty dictionary.

        Returns:
            json: The email metadata, or an empty dictionary if no email sender exists.
        """
        self._log_debug_trace_format()
        if not self._email_sender:
            return {}
        return self._meta_data

    @property
    def payload(self) -> json:
        """
        Returns the email payload as a JSON-serializable dictionary.

        This method dynamically constructs the payload from the current state of 
        the email sender. It can be used before the email is sent to preview the payload.
        
        Raises:
            InvalidPayload: If the constructed payload is not valid.
        
        Note: The method is not chainable because it assumes the user
        might want to do something with the data
        """
        if not self._email_sender:
            return {}

        # Dynamically create the payload—useful for previewing before sending
        if self._fields_marked_for_reset:
            email_payload = self._email_payload
        else:
            email_payload = EmailPayload(
                from_email=self._email_sender.from_email,
                to_email=self._email_sender.to_email,
                subject=self._email_sender.subject,
                body_html=self._email_sender.html_template,
                body_text=self._email_sender.text_template,
                context=self._email_sender.context,
                headers=self._email_sender.headers
            )

        if not email_payload.is_valid():
            raise InvalidPayload(EmailMessages.ERROR_OCCURED)

        return email_payload.to_json()

    def _log_message(self, msg: str, logger_type: str = LoggerType.INFO, exc: Exception = None, *args, **kwargs) -> None:
        """
        Logs a message using the configured logger, with optional exception handling and message formatting.

        Args:
            msg (str): The message to log. Can include placeholders for formatting with *args and **kwargs.
            logger_type (str, optional): The type of log to emit. Valid options are defined in LoggerType 
                                        ('error', 'warning', 'info'). Defaults to 'info'.
            exc (Exception, optional): An exception instance to include in the log. If provided, a traceback 
                                    will be appended or passed to a custom formatter (if configured).
            *args: Optional positional arguments to format the message string.
            **kwargs: Optional keyword arguments to format the message string.

        Behaviour:
            - If a logger is configured and logging is enabled, the message is dispatched to the appropriate
            logger method (e.g., logger.error, logger.warning).
            - If an exception is passed, the message will include traceback information or be formatted via a
            custom formatter (if one is set).
            - If no logger is configured, the method exits silently.

        """
        if not self._logger:
            return

        if not isinstance(logger_type, (LoggerType, str)): 
            return

        formatted_msg = translate_message(msg, *args, **kwargs)
        
        if exc is not None:
            formatted_msg = self._add_traceback(exc, msg)
    
        if self._logging_enabled:
            self._dispatch__log_message(formatted_msg, logger_type, *args, **kwargs)

    def _add_traceback(self, exc: Exception, msg: str) -> str:
        """
        Appends traceback information to the message if enabled and available.

        Using the `show_traceback` which is set by the user (True or False) determinees if
        a traceback should be added.

        Args:
            msg (str): The message to which the traceback will be appended.

        Returns:
            str: The original message with the appended traceback information (if any).
        """

        trace = format_exc()

        if self._show_traceback_error and trace and "NoneType: None" not in trace:
            msg += f"\nTraceback:\n{trace}"
            
        if self._custom_formatter:
            msg = self._custom_formatter(exc, trace)
        return msg

    def _log_debug_verbose(self, msg, logger_type=LoggerType.DEBUG, *args, **kwargs):
        """
        Logs a verbose debug message if the debug verbose mode is enabled. These
        are extra message information that are only show when the `.enable_verbose()`
        is turned on.

        Args:
            msg (str): The message to be logged.
            logger_type (LoggerType, optional): The type of logger to use (defaults to `LoggerType.DEBUG`).
            *args: Additional positional arguments to be passed to the logging method.
            **kwargs: Additional keyword arguments to be passed to the logging method.

        Returns:
            None
        """
        if not self._logging_enabled:
            self._dispatch__log_message(LoggerMessages.NOT_ENABLED, LoggerType.DEBUG)
            return
    
        if self._debug_verbose:
            self._dispatch__log_message(msg, logger_type, *args, **kwargs)

    def _dispatch__log_message(self, msg, logger_type, *args, **kwargs):
        """
        Dispatches a formatted log message to the appropriate logging method.

        This method first formats the provided message using the `translate_message` function,
        into a language that can be translated to any of the supported languages, and then selects 
        the correct logging method based on the `logger_type` provided e.g 'DEBUG', 'ERROR', etc. 
        If the logging method is found, it calls the method to log the message ar raises 
        an exception if occurs during the process, it silently ignores the error.

        Args:
            msg (str): The message to be logged.
            logger_type (LoggerType): The type of logger to determine which logging method to use.
                                      e.g. 'DEBUG', 'ERROR', etc.
            *args: Additional positional arguments to be passed to the message formatting function.
            **kwargs: Additional keyword arguments to be passed to the message formatting function.

        Returns:
            None
        """
        try:
            
            formatted_msg = translate_message(msg, *args, **kwargs)
            log_method    = self._get_log_method(logger_type)  
                       
            if log_method:
                log_method(formatted_msg)
                
        except Exception as e:
            self._log_message("ERROR - {e}", LoggerType.DEBUG, e=str(e))
       

    def _get_log_method(self, logger_type: str):
        """
        Retrieves the logging method based on the specified logger type.

        Args:
            logger_type (str): The type of logger (e.g., 'debug', 'info', 'error') to retrieve.

        Returns:
            Callable or None: The corresponding logging method if found, otherwise `None`.
        """
        return getattr(self._logger, logger_type.lower(), None)

    def _get_field_audit(self) -> dict:
        """
        Retrieves a copy of the field changes audit data.

        This method returns a copy of the `_field_changes` dictionary, which contains the
        audit trail of changes made to fields e.g subject, from_email, etc. 
        A copy is return which ensures that the original audit data cannot be modified directly.

        Returns:
            dict: A copy of the field changes audit data.
        """
        return self._field_changes.copy()

    def _load_template_preview_in_logger(self, preview_chars: int = 100) -> str:
        """
        Safely loads an HTML or text email template and returns a preview snippet.

        Args:
            path (Union[str, Path]): The path to the template file.
            preview_chars (int): The number of characters to preview from the template.

        Returns:
            str: A truncated preview of the template contents.

        Logs a warning if the file cannot be read.
        """
        self._log_debug_trace_format()
        
        try:
            html_path, text_path = self._get_html_and_text_file_path()
            
            self._log_debug_verbose("Retrieved html_path {html} and text_path {text_path} from '_get_html_and_text_file_path()' ", 
                                    html=html_path, text_path=text_path)
            
            if html_path is None or text_path is None:
                self._if_template_path_are_missing_log_and_raise_exception(html_path=html_path, text_path=text_path)
            
            self._set_template_preview(html_path=html_path, text_path=text_path)
            
            if self._enable_field_trace_logging and EmailSenderConstants.Fields.HTML_TEMPLATE.value not in self._fields:
                return
            
        except Exception as e:
            
            self._log_message(FieldMessages.FIELDS_MISSING, LoggerType.ERROR, exc=e)
            raise EmailSenderBaseException(message=str(e))
       
    def _if_template_path_are_missing_log_and_raise_exception(self, html_path, text_path):
        """
        Logs an error message and raises an exception if the template paths are missing.

        This method checks if the `html_path` and `text_path` are missing. It logs an error message 
        containing the missing template paths and then raises an `EmailSenderBaseException` with 
        details about the missing paths.

        Args:
            html_path (str): The path to the HTML template.
            text_path (str): The path to the text template.

        Raises:
            EmailSenderBaseException: If either of the template paths is missing, an exception is raised 
            with details about the missing fields.
        """
        
        self._log_message(ConfigMessages.MISSING_CONFIG, LoggerType.ERROR)
        
        error_msg = TemplateMessages.MISSING_TEMPLATES.format(html=html_path, text=text_path)
        
        self._log_message(error_msg, LoggerType.ERROR)
                
        raise EmailSenderBaseException(error_msg)
    
    def _set_template_preview(self, html_path, text_path, preview_chars=100):
        """
        Sets the HTML and text preview for the provided template paths.

        This method retrieves the content from the given HTML and text template paths, 
        generates a preview for each (up to a specified number of characters), 
        and logs the preview content. If no preview is available, it logs a 
        message indicating that no preview is available for the respective template.

        Args:
            html_path (str): The path to the HTML template file.
            text_path (str): The path to the text template file.
            preview_chars (int): The number of characters to display in the preview.

        Returns:
            tuple: A tuple containing two strings:
                - html_preview (str): The preview of the HTML template.
                - text_preview (str): The preview of the text template.

        Logs:
            - Logs the HTML and text preview content.
            - Logs a message if a preview is not available for either template.
        """
        HAS_PREVIEW  = "No '{preview}' preview available"
        
        self._log_debug_trace_format()
        
        html_preview = get_html_preview(self._read_content_from_file(html_path), preview_chars)
        text_preview = get_safe_text_preview(self._read_content_from_file(text_path), preview_chars)

        # check if a preview is available, if not shows the 'HAS_PREVIEW' message.
        self._text_preview = text_preview or translate_message(HAS_PREVIEW, ".html")
        self._html_preview = html_preview or translate_message(HAS_PREVIEW, ".txt")
        
        self._log_message("[TEMPLATES][SET_TEMPLATE_PREVIEW] text_preview {text_preview}, html_preview {html_preview}", 
                          text_preview=text_preview, html_preview=html_preview)
        
        self._log_message(TemplateMessages.HTML_PREVIEW, html_preview=html_preview)
        self._log_message(TemplateMessages.PLAIN_TEXT_PREVIEW, text_preview=text_preview)

        return html_preview, text_preview
    
    def _read_content_from_file(self, file_path):
        """
        Reads the content of a file at the specified path.

        This method first attempts to open and read the content of the file located at the
        given `file_path`. If the file is found, it returns its content as a string.
        If the file is not found, it logs an exception and returns a message indicating
        that the file could not be found.

        Args:
            file_path (str): The path to the file whose content is to be read.

        Returns:
            str: The content of the file if it exists, or a message indicating the file
                was not found.

        Logs:
            - Logs an exception if the file is not found at the specified path.
        """
        try:
        
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            return content
        
        except FileNotFoundError as e:
            self._log_message(translate_message("The file path couldn't be found: {e}", e=e), exc=e)
        return translate_message("The file wasn't found")

    def _get_html_and_text_file_path(self) -> tuple:
        """
        Retrieves the HTML and text template file paths from the email sender.

        This method attempts to retrieve the paths to the HTML and text template files
        from the email sender. If either file path is missing or an error occurs during
        the retrieval process, it logs the failure and returns `None, None`. If both paths
        are found, it logs their successful retrieval and returns the paths as a tuple.

        Returns:
            tuple: A tuple containing two strings:
                - html_path (str): The path to the HTML template file.
                - text_path (str): The path to the text template file.
            
            If either path is missing or an exception occurs, returns `(None, None)`.

        Logs:
            - Logs an attempt to retrieve the file paths.
            - Logs the success or failure of retrieving the HTML and text file paths.
            - Logs the actual file paths if retrieval is successful.
        """
        
        self._log_debug_trace_format()
        self._log_debug_verbose(LogExecutionMessages.VERBOSE_ATTEMPT_RETRIEVE, LoggerType.INFO)
       
        try:
            html_path = self._email_sender.html_template
            text_path = self._email_sender.text_template
            
        except EmailSenderBaseException as e:
            self._log_debug_verbose(LogExecutionMessages.VERBOSE_RETRIEVE_FAILED, LoggerType.ERROR, html=None, text=None)
            self._log_message(str(e), LoggerType.ERROR, exc=e)
            return None, None
      
        if html_path is None:
            self._log_debug_verbose(TemplateMessages.MISSING_HTML_FILE)
            self._log_message(TemplateMessages.MISSING_HTML_FILE, LoggerType.ERROR)
            return None, None

        if text_path is None:
            self._log_debug_verbose(TemplateMessages.MISSING_TEXT_FILE, LoggerType.ERROR)
            return None, None
        
        if html_path is None or text_path is None:
            return

        self._log_debug_verbose(TemplateMessages.HTML_TEMPLATE_PATH, LoggerType.INFO, html=html_path)
        self._log_debug_verbose(TemplateMessages.TEXT_TEMPLATE_PATH, LoggerType.INFO, text=text_path)
        self._log_debug_verbose(TemplateMessages.TEMPLATE_RETREIVED, LoggerType.INFO)
        
        return html_path, text_path
 
    def _log_email_summary(self, additional_recipients, time_taken, status, emails_sent_count, timestamp, attachments=None) -> str:
        """
        Logs a detailed summary of the email sending operation.

        This method logs a structured log summary containing key metadata about the email,
        such as sender, recipients, templates used, and previews. It also reports performance
        metrics like time taken and delivery status, as well as internal field 
        tracking such as fields logged and skipped.

        Args:
            additional_recipients (list): List of email addresses.
            time_taken (float): Duration in seconds it took to process and send the email.
            status (bool): Whether the email was successfully sent (`True`) or failed (`False`).
            emails_sent_count (int): Number of recipients to whom the email was actually sent.
            timestamp (datetime): Timestamp when the email was processed.
            attachments (list, optional): List of attached file names, if any. Defaults to `None`.

        Logs:
            - A structured breakdown of email metadata including subject, sender, recipients, and templates.
            - Summary of HTML/text previews and delivery result.
            - Diagnostics about the fields logged vs skipped and internal flags for header/context readiness.
            - Overall success or failure of the operation.

        Returns:
            str: (Implicitly returns `None`, but could return summary string if needed in the future.)
            
        """

        skipped        = self._get_num_of_skipped_fields()
        status_message = "Successfully sent" if status else "Failed to send email"
        
        fields = ", ".join(self._fields)
        skipped_fields = ", ".join(self._exclude_fields)
        
        self._log_message(EmailLogSummary.HEADER_LINE)
        self._log_message(EmailLogSummary.SPACE)
        self._log_message(EmailLogSummary.TITLE)
        self._log_message(EmailLogSummary.HEADER_LINE)
        self._log_message(EmailLogSummary.EMAIL_ID, email_id=self._email_sender.email_id)
        self._log_message(EmailLogSummary.TIMESTAMP, timestamp=timestamp)
        self._log_message(EmailLogSummary.LANGUGAGE_SENT, language=settings.LANGUAGE_CODE)
        self._log_message(EmailLogSummary.SUBJECT, subject=self._email_payload.subject)
        self._log_message(EmailLogSummary.FROM, from_email=self._email_payload.from_email)
        self._log_message(EmailLogSummary.TO, to_email=self._email_payload.to_email)
        self._log_message(EmailLogSummary.ADDITIONAL_RECIPIENTS, additional_recipients=additional_recipients)
        self._log_message(EmailLogSummary.TOTAL_RECIPIENTS, total_recipients=len(additional_recipients) + 1)
        self._log_message(EmailLogSummary.HTML_TEMPLATE, html_template=self._email_payload.body_html)
        self._log_message(EmailLogSummary.TEXT_TEMPLATE, text_template=self._email_payload.body_text)
        self._log_message(EmailLogSummary.HTML_SHORT_NAME, html_name=self._field_changes.get("short_html_name"))
        self._log_message(EmailLogSummary.TEXT_SHORT_NAME, text_name=self._field_changes.get("short_text_name") )
        self._log_message(EmailLogSummary.ATTACHMENTS, attachments=attachments)
        self._log_message(EmailLogSummary.ENVIRONMENT, environment=self._get_environment())
        self._log_message(EmailLogSummary.TIME_TAKEN, time_taken=time_taken)
        self._log_message(EmailLogSummary.STATUS, status_message=status_message)
        self._log_message(EmailLogSummary.DELIVERED, delivered=emails_sent_count)
        self._log_message(EmailLogSummary.TEXT_PREVIEW, text_preview=self._text_preview)
        self._log_message(EmailLogSummary.HTML_PREVIEW, html_preview=self._html_preview)
        self._log_message(EmailLogSummary.EMAIL_FORMAT)
        self._log_message(EmailLogSummary.BOTTOM_LINE)
        self._log_message(EmailLogSummary.SPACE)
                

        self._log_message(FieldSummaryLog.END_SUMMARY)
        self._log_message(EmailLogSummary.SPACE)
        self._log_message(EmailLogSummary.SPACE)
        self._log_message(FieldSummaryLog.FIELDS_LOG_AND_SKIPPED, fields=fields, num_skipped=skipped)       
        self._log_message(FieldSummaryLog.FIELDS_LOGGED, count=self._get_num_of_logged_fields())
        self._log_message(FieldSummaryLog.FIELDS_SKIPPED, count=skipped, fields_skipped=skipped_fields)
        self._log_message(FieldSummaryLog.FIELDS_SUMMARY,  headers_set=self._is_headers_set, context_set=self._is_context_set)
        self._log_message(FieldSummaryLog.END_SUMMARY)
        self._log_message(EmailLogSummary.SPACE)
           
    def log_only_fields(self, *fields):
        """
        Enables selective logging for specific fields during trace logging.

        This method configures the logger to record only the specified fields when 
        generating field-level logs. It disables any existing exclusion-based logging 
        to ensure only the provided fields are tracked.
        
        Note:
            You can manually enter the fields by hand, however, that is more error prone,
            a less error prone way is to import the enum `EmailSenderConstants` class
            which contains all the fields and simply use it. Since it is an enum
            class, ensure that you are using '.value' at the end to get string value.

        Args:
            *fields (str): One or more field names to include in the logging output.

        Returns:
            self: Enables method chaining for fluent API usage.

        Example:
            from django_email_sender.email_sender_constants import EmailSenderConstants
            
            logger.log_only_fields(EmailSenderConstants.Field.Subject.value, EmailSenderConstants.Fields.TO_EMAIL.value)
        """
        self._enable_field_trace_logging   = True
        self._enable_exclusion_field_trace = False  
      
        self._fields = set(fields)
        return self
    
    def exclude_fields_from_logging(self, *fields):
        """
        Enables exclusion-based field logging.

        This method configures the logger to skip logging for the specified fields during 
        trace logging. It disables any inclusion-based logging to ensure that all fields 
        are logged except the ones provided.

        Note:
            You can manually enter the fields by hand, however, that is more error prone,
            a less error prone way is to import the enum `EmailSenderConstants` class
            which contains all the fields and simply use it. Since it is an enum
            class, ensure that you are using '.value' at the end to get string value.
            
        Args:
            *fields (str): One or more field names to exclude from the logging output.

        Returns:
            self: Enables method chaining for fluent API usage.

        Example:
            exclude_fields_from_logging(EmailSenderConstants.Field.Subject.value, 
                                              EmailSenderConstants.Fields.TO_EMAIL.value)
        """
        self._enable_field_trace_logging = False
        self._enable_exclusion_field_trace = True
        self._exclude_fields = set(fields)
        return self
    
    def reset_field_logging_filters(self):
        """
        Resets all field logging filters to their default state.

        This method disables both inclusion-based and exclusion-based field logging,
        allowing all fields to be logged without restriction.

        Returns:
            self: Enables method chaining for fluent API usage.

        Example:
            reset_field_logging_filters()
        """
        self._enable_field_trace_logging   = False
        self._enable_exclusion_field_trace = False
        self._fields                       = set()
        self._exclude_fields               = set()
        return self

    def _clear_methods_seen(self):
        self._methods_seen = []
        
    def _log_to_db(self) -> bool:
        """
        Logs the email details to the database using the provided log model.
        Returns True if logging was successful, otherwise does nothing.
        """
    
        if self._log_model is None or self._email_was_processed is None:
            return False  
        
        self._log_debug_trace_format()
        log_model = self._log_model()  

        if self._fields_marked_for_reset:
            log_model.to_email   = self._email_payload.to_email
            log_model.from_email = self._email_payload.from_email
            log_model.subject    = self._email_payload.subject
                                 
        else:
            log_model.to_email   = self._email_sender.to_email
            log_model.from_email = self._email_sender.from_email
            log_model.subject    = self._email_sender.subject
        
        log_model.email_body = self._text_preview
        log_model.status     = self._was_sent_successfully

        try:
            
            log_model.save()
            self._email_was_processed = None  # Reset state
            return True
        
        except IntegrityError as e:
            self._log_message(EmailMessages.EMAIL_NOT_SAVED_TO_DB,  
                              from_email=self._email_sender.from_email,
                              recipient=self._email_sender.to_email,
                              subject=self._email_sender.subject,
                              body_summary=self._html_preview,
                              exc=e
                              )
            raise EmailSenderBaseException(message=str(e))
       
    def _get_num_of_skipped_fields(self):
        """Returns the number of fields that were skipped"""
        return len(self._exclude_fields)
    
    def _get_num_of_logged_fields(self):
        """Return the number of fields that were logged"""
        return len(self._fields)
     
            