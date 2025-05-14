from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from typing import List, Optional, Dict, Union
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pathlib import Path
from os.path import join, exists
from secrets import token_hex

from django_email_sender.exceptions import (
    EmailTemplateNotFound,
    TemplateDirNotFound,
    ContextIsNotADictionary,
    EmailSenderBaseException,
    EmailSendError,
    IncorrectEmailSenderFieldType,
   
)

from django_email_sender.messages import TemplateMessages, EmailMessages, ContextMessages, FieldMessages
from django_email_sender.email_sender_constants import EmailSenderConstants
from .utils import get_template_dirs
from .translation import safe_set_language


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dirs                = get_template_dirs()
TEMPLATES_DIR       = dirs["TEMPLATES_DIR"]
EMAIL_TEMPLATES_DIR = dirs["EMAIL_TEMPLATES_DIR"]


class EmailSender:
    """
    An email sender that allows you to send emails by
    using a chaining method. This is mostly to be used in
    the Django eco-system.

    To use it in a Django eco-system, the following settings must be configured:

    settings.py:
    
    EMAIL_BACKEND       = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS       = True  
    EMAIL_HOST          = 'host'  
    EMAIL_PORT          = 587  
    EMAIL_HOST_USER     = 'some@emailhere.com'  
    EMAIL_HOST_PASSWORD = 'password'

    templates:
        - Specify paths to your email templates.

    Example usages:
        You can easily abstract the `EmailSender` class into specific methods for sending different types of emails.
        
        For example, to send a verification email:
        
        def send_verification_email(user):
        
            subject = "Verify Your Email"
            from_email = "no-reply@example.com"

            return EmailSender.create()\
                .from_address(from_email)\
                .to([user.email])\
                .with_subject(subject)\
                .with_context({
                    "username": user.username, 
                    "verification_link": generate_verification_link(user)
                })\
                .with_text_template(folder_name="email", template_name="verification.txt")\
                .with_html_template(folder_name="email", template_name="verification.html")\
                .send()

        Similarly, you can create other email methods such as:
        
        def send_registration_email(user):
          
            subject    = "Welcome to the Platform!"
            from_email = "no-reply@example.com"

            return EmailSender.create()\
                .from_address(from_email)\
                .to([user.email])\
                .with_subject(subject)\
                .with_context({"username": user.username})\
                .with_text_template(folder_name='emails', template_name='registration.html')\
                .with_html_template(folder_name='emails', template_name='registeration.txt')\
                .send()
                
        This approach allows you to abstract email sending into different functions for 
        various use cases (e.g., registration, verification, password reset), 
        but at the same time allows the email sender class to be a single source of truth while allowing the
        sending logic clean, consistent, and reusable.
    """

    def __init__(self):
        """
        Initialize an empty email configuration.
        """
        self.from_email: Optional[str]    = None
        self.to_email: str                = None
        self.subject: Optional[str]       = None
        self.html_template: Optional[str] = None
        self.text_template: Optional[str] = None
        self.context: Dict[str, str]      = {}
        self.headers: Dict[str, str]      = {}
        self.list_of_recipients           = set()
        self.email_id                     = token_hex()
      
        self.fields_to_reset = {
            EmailSenderConstants.Fields.FROM_EMAIL.value: None,
            EmailSenderConstants.Fields.TO_EMAIL.value: [],
            EmailSenderConstants.Fields.SUBJECT.value: None,
            EmailSenderConstants.Fields.HTML_TEMPLATE.value: None,
            EmailSenderConstants.Fields.TEXT_TEMPLATE.value: None,
            EmailSenderConstants.Fields.CONTEXT.value: {},
            EmailSenderConstants.Fields.HEADERS.value: {},
        }

        safe_set_language()
            
    @classmethod
    def create(cls) -> "EmailSender":
        """
        Class factory method to initialize the EmailSender for method chaining.

        Returns:
            EmailSender: A new instance of EmailSender.
        """
        return cls()

    def from_address(self, email: str) -> "EmailSender":
        """
        Set the sender's email address.

        Args:
            email (str): The sender's email address.

        Returns:
            EmailSender: The current instance for chaining.
        """
        if not email:
            return self
        
        self.from_email = email
        return self

    def to(self, recipient:  Optional[Union[str, List[str]]]) -> "EmailSender":
        """
        Set the recipient(s) of the email.

        sets a single recipient to the recipient field. 

        Args:
            recipients (Union[str, List[str]]): A single email address or a list of email addresses.
            Note:
              The list has been left to maintain backwards compatibility. If you add a list
              of emails e.g ["first_email@example.com", "second_email@example.com"] only the
              first email will be used "first_email@example.com".
              
              If you want to add multiple emails use the `.add_new_recipient()` method.
              
              Do not call the method `.to(...)` to add multiple emails because it will only change
              the `to_email` not add to it.

        Returns:
            EmailSender: The current instance for chaining.
        """
        if not recipient:
            return self
        
        if isinstance(recipient, list) and recipient:
            self.to_email = recipient[0]
        else:
            self.to_email = recipient
        return self

    def with_subject(self, subject: str) -> "EmailSender":
        """
        Set the subject of the email.

        Args:
            subject (str): The subject line.

        Returns:
            EmailSender: The current instance for chaining.
        """
      
        self.subject = subject 
        return self

    def with_context(self, context: Dict) -> "EmailSender":
        """
        Set the context dictionary for rendering templates.

        Args:
            context (Dict): Context variables for use in templates.

        Returns:
            EmailSender: The current instance for chaining.
        """

        if not isinstance(context, dict):
            raise ContextIsNotADictionary(ContextMessages.format_message(msg=ContextMessages.CONTEXT_ERROR, 
                                                                         context=context, 
                                                                         context_type=type(context)
                                                                         ))

        self.context = context
        
        return self

    def with_html_template(self, template_name: str, folder_name: str = None) -> "EmailSender":
        """
        Set the HTML template path.

        Args:
            template_name (str): The name of the plain text template file (e.g. 'welcome.html').
            folder_name (str, optional): The name of the subfolder inside the 'email_templates' directory
                                        where this template is located. If None, template is assumed to
                                        reside directly in the 'email_templates' folder.

        Returns:
            EmailSender: The current instance for chaining.
        """
        if not template_name:
            return self
         
        self.html_template = self._create_path(template_name, folder_name)
        return self

    def with_text_template(self, template_name: str, folder_name: str = None) -> "EmailSender":
        """
        Set the plain text template path for the email.

        Args:
            template_name (str): The name of the plain text template file (e.g. 'welcome.txt').
            folder_name (str, optional): The name of the subfolder inside the 'email_templates' directory
                                        where this template is located. If None, template is assumed to
                                        reside directly in the 'email_templates' folder.

        Returns:
            EmailSender: The current instance for method chaining.
        """
        
        self.text_template = self._create_path(template_name, folder_name)
        return self

    def add_new_recipient(self, recipient: str) -> "EmailSender":
        """
        Adds an additional email recipient to the list of recipients.

        This method ensures no duplicate recipients are added by storing 
        them internally in a set.

        Args:
            recipient (str): The email address to add as a recipient.
         """
        
        if not recipient or recipient is None:
            return self 
        
        if not isinstance(recipient, str):
            raise IncorrectEmailSenderFieldType(FieldMessages.FIELD_TYPE_IS_INCORRECT, expected_type=recipient, received_type=type(recipient))
            
        self.list_of_recipients.add(recipient)
        return self
            
    def _raise_if_template_path_not_found(self, email_path: str) -> None:
        """
        Checks whether a given template path exists within the email templates directory.

        This method performs the following checks:
        - Ensures the base template directory exists (e.g., TEMPLATES_DIR).
        - Ensures the 'email_templates' folder exists within the base directory.
        - Confirms the specific template file exists at the given path.

        Args:
            email_path (str): The full relative path to the template file to check.

        Raises:
            TemplateDirNotFound: If the base template directory is missing.
            EmailTemplateDirNotFound: If the 'email_templates' folder is missing.
            TemplateNotFound: If the given email template file does not exist.
        """
     
        if not exists(TEMPLATES_DIR):
            raise TemplateDirNotFound(message=TemplateMessages.PRIMARY_TEMPLATE_MISSING)

        if not exists(EMAIL_TEMPLATES_DIR):
            raise EmailTemplateNotFound(message=TemplateMessages.format_message(TemplateMessages.EMAIL_TEMPLATE_NOT_FOUND, path=EMAIL_TEMPLATES_DIR))

        if not exists(email_path):
            raise EmailTemplateNotFound(message=TemplateMessages.format_message(TemplateMessages.TEMPLATE_NOT_FOUND, path=email_path))

    def _create_path(self, template_name: str, folder_name: str = None):
        """
        Constructs the full path to an email template file inside the 'email_templates' directory.

        Allows for an optional subfolder to help organise templates by category (e.g., registration, password_reset).

        Args:
            template_name (str): Name of the template file (e.g., 'welcome.html').
            folder_name (str, optional): Name of the subfolder inside 'email_templates'. Defaults to None.

        Returns:
            str: The combined relative path to the desired template.

        Raises:
            ValueError: If template_name is not a string, or folder_name is not a string or None.
        """

        if folder_name is not None and not isinstance(folder_name, str):
            error_msg = _("The folder path must be a string or None. Got type '{folder_type}' for folder")
            raise EmailSenderBaseException(error_msg.format(folder_type=type(folder_name).__name__))

        if template_name is not None and not isinstance(template_name, str):
            error_msg = _("The template name path must be a string or None. Got type '{template_type}' for folder")
            raise EmailSenderBaseException(error_msg.format(template_type=type(template_name).__name__))

        if folder_name is None:
            return join(EMAIL_TEMPLATES_DIR, template_name)  
        return join(EMAIL_TEMPLATES_DIR, folder_name, template_name)
      
    def with_headers(self, headers: Dict) -> "EmailSender":
        """
        Set custom headers for the email.

        Args:
            headers (Optional[Dict], optional): A dictionary of headers to include in the email. Default is an empty dictionary.

        Raises:
            TypeError: If headers is not a dictionary.

        Returns:
            EmailSender: The current instance for chaining.
        """
        if headers is None:
            headers = {}
                      
        if not isinstance(headers, dict):
            error_msg = _("'Headers' must be a dictionary but got type '{headers_type}' instead")
            raise EmailSenderBaseException(error_msg.format(headers_type=type(headers).__name__))
                
        self.headers = headers
        return self

    def _validate(self):
        """ """
        if not all([self.from_email, self.to_email, self.subject, self.html_template, self.text_template]):
            
            error_msg =  _("All email components (from, to, subject, html, text) must be set before sending.")
            raise EmailSenderBaseException(error_msg)

        self._raise_if_template_path_not_found(TEMPLATES_DIR)
        self._raise_if_template_path_not_found(EMAIL_TEMPLATES_DIR)
        self._raise_if_template_path_not_found(self.text_template)
        self._raise_if_template_path_not_found(self.html_template)

    def clear_from_email(self) -> "EmailSender":
        """Clears the field of the sender"""
        self.from_email = None
        return self

    def clear_to_email(self) -> "EmailSender" :
        """Clears the recipient field"""
        self.to_email = []
        return self

    def clear_subject(self) -> "EmailSender":
        """Clear the subject"""
        self.subject = None
        return self

    def clear_context(self) -> "EmailSender":
        """Clear the context field"""
        self.context = {}
        return self

    def clear_html_template(self) -> "EmailSender":
        """clear the html template path"""
        self.html_template = None
        return self

    def clear_text_template(self) -> "EmailSender":
        """clear the text template path"""
        self.text_template = None
        return self

    def clear_headers(self) -> "EmailSender":
        """Clear the headers"""
        self.headers = {}
        return self
    
    def clear_all_fields(self)  -> "EmailSender":
        """Clear all the fields"""

        for field_name, default_field in self.fields_to_reset.items():
            setattr(self, field_name, default_field)
        return self

    def _get_recipients(self):
        """
        Returns a combined list of email recipients.

        This includes the primary recipient `self.to_email` (if provided and not None)
        and any additional recipients from `self.list_of_recipients`.

        Returns:
            list: A list of recipient email addresses.
        """
        recipients = []
        
        if self.to_email:
            recipients.append(self.to_email)
        if self.list_of_recipients:
            recipients.extend(self.list_of_recipients)
        return recipients

    def send(self, auto_reset: bool = False) -> int:
        """
        Send the email using Django's email backend.

        This will render the text and HTML templates, attach the HTML alternative, and send the email.

        Args:
            auto_reset (bool): If auto_reset is True, the instance is reset after sending.

        Raises:
            ValueError: If any required fields are missing before sending.
            EmailSendError: Raises an EmailSendError if an error occurs while sending an email.

        Returns:
            int: The number of successfully delivered messages (typically 1 if successful).
        """
        self._validate()
            
        text_content = render_to_string(self.text_template, context=self.context)
        html_content = render_to_string(self.html_template, context=self.context)

        msg = EmailMultiAlternatives(
            subject=self.subject,
            body=text_content,
            from_email=self.from_email,
            to=self._get_recipients(),
            headers=self.headers or {},
        )
     
        msg.attach_alternative(html_content, "text/html")

        try:
            resp = msg.send()
            is_sent = True if resp > 0 else False
            if auto_reset:
                self.clear_all_fields()
    
            return (resp, is_sent)

        except EmailSendError as e:
            error_msg = EmailMessages.FAILED_TO_SEND_EMAIL.format(from_user=self.from_address, to_user=self.to, error=str(e))
            raise EmailSendError(message=error_msg)
        except EmailSenderBaseException as e:
          raise EmailSendError(message=EmailMessages.ERROR_OCCURED, e=_("Something went wrong and the email wasn't sent"))

