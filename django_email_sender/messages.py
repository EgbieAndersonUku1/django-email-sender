from dataclasses import dataclass
from django.utils.translation import gettext_lazy as _



class BaseFormatter:
    @staticmethod
    def format_message(msg: str, **kwargs) -> str:
        """
        Retrieves the formatted message with the provided arguments.

        Args:
            msg (str): The message template to format.
            **kwargs: Arguments to format the message with.

        Returns:
            str: The formatted message.
        """
        try:
            return msg.format(**kwargs)
        except (IndexError,  KeyError):
            return msg
          
    def list_messages(self) -> dict:
        """
        Returns a dictionary of all message keys and their string values.

        Returns:
            dict: A dictionary of message name -> message template string.
        """
        return {
            key: getattr(self, key) for key in dir(self) if not key.startswith("_") and isinstance(getattr(self, key), str)
        }


# ────────────────────────────────
# Template & Folder Related Logs
# ────────────────────────────────
@dataclass(frozen=True)
class TemplateMessages(BaseFormatter):
    USING_DEFAULT_FOLDER      : str = _("No folder specified. Using default: '{default_folder}'. | category=TEMPLATE | action=DEFAULT_FOLDER")
    OVERRIDE_FOLDER           : str = _("Folder '{folder_name}' selected instead of default '{default_folder}'. | category=TEMPLATE | action=OVERRIDE_FOLDER")
    LOADING_TEMPLATE          : str = _("Loading email template from: '{path}'. | category=TEMPLATE | action=LOADING")
    CREATING_PATH             : str = _("Creating path for template: '{template}', folder: '{folder}'. | category=TEMPLATE | action=CREATING_PATH")
    TEMPLATE_NOT_FOUND        : str = _("Failed to locate email template at: '{path}'. | category=TEMPLATE | action=NOT_FOUND")
    PRIMARY_TEMPLATE_MISSING  : str = _("Primary template [Templates] is missing,  category=TEMPLATE, action=MISSING_PRIMARY")
    EMAIL_TEMPLATE_NOT_FOUND  : str = _("Failed to locate 'email template' path at '{path}'. | category=TEMPLATE | action=EMAIL_NOT_FOUND")
    FALLBACK_TEMPLATE         : str = _("Primary template unavailable. Falling back to backup template. | category=TEMPLATE | action=FALLBACK")
    TEMPLATES_NOT_FOUND       : str = _("The folder and email template were not found. | category=TEMPLATE | action=ALL_NOT_FOUND")
    HTML_PREVIEW              : str = _("'HTML template preview' (first 100 characters): {html_preview}. | category=TEMPLATE | action=HTML_PREVIEW")
    PLAIN_TEXT_PREVIEW        : str = _("'Plain text template preview' (first 100 characters): {text_preview}. | category=TEMPLATE | action=TEXT_PREVIEW")
    MISSING_TEMPLATES         : str = _("html field {html} and text field {text} are missing. | category=TEMPLATE | action=MISSING_FIELD")
    MISSING_HTML_FILE         : str = _("HTML file is missing (got None). | category=TEMPLATE | action=MISSING_FILE")
    MISSING_TEXT_FILE         : str = _("Text file is missing (got None). | category=TEMPLATE | action=MISSING_FILE")
    HTML_TEMPLATE_PATH        : str = _("HTML file path: {html}. | category=TEMPLATE | action=TEMPLATE_PATH")
    TEXT_TEMPLATE_PATH        : str = _("Text file path: {text}. | category=TEMPLATE | action=TEMPLATE_PATH")
    TEMPLATE_RETREIVED        : str = _("Successfully retrieved HTML and text file paths. | category=TEMPLATE | action=TEMPLATE_PATH")

    def __str__(self) -> str:
        return _("TemplateMessages: A collection of email template-related message templates.")



# ────────────────────────────────
# EmailMessages
# ────────────────────────────────
@dataclass(frozen=True)
class EmailMessages(BaseFormatter):
    START_EMAIL_SEND                  : str = _("Starting email sending process... | category=EMAIL | action=SEND_START")
    CHECK_FOR_LIST_OF_EMAIL_RECIPIENT : str = _("Checking for a list of recipients. | category=EMAIL | action=RECIPIENT_CHECK")
    FOUND_NUM_OF_RECIPIENT            : str = _("Found {num} additional recipients to send to. | category=EMAIL | action=RECIPIENT_FOUND")
    LIST_OF_RECIPIENTS                : str = _("Additional recipients: {list_of_recipients}. | category=EMAIL | action=RECIPIENT_LIST")
    SENDER_EMAIL                      : str = _("The email will be sent from: '{sender_email}'. | category=EMAIL | action=SENDER")
    SEND_TO_EMAIL                     : str = _("The email will be sent to: '{to_email}'. | category=EMAIL | action=TO_EMAIL")
    MULTIPLE_RECIPIENTS               : str = _("Multiple recipients provided: {to_email}. | category=EMAIL | action=MULTIPLE_RECIPIENTS")
    SINGLE_RECIPIENT                  : str = _("Single recipient 'set': {to_email}. | category=EMAIL | action=SINGLE_RECIPIENT")
    SUBJECT_LINE                      : str = _("Email subject: '{subject}'. | category=EMAIL | action=SUBJECT")
    EMAIL_FORMAT                      : str = _("Email format: multipart/alternative (HTML + plain text). | category=EMAIL | action=EMAIL_FORMAT")
    HTML_TEMPLATE_USED                : str = _("HTML template used: '{html_template_path}'. | category=EMAIL | action=TEMPLATE_HTML")
    TEXT_TEMPLATE_USED                : str = _("Text template used: '{text_template_path}'. | category=EMAIL | action=TEMPLATE_TEXT")
    EMAIL_SEND_COMPLETE               : str = _("Email sent successfully. | category=EMAIL | action=SEND_COMPLETE")
    FAILED_TO_SEND_EMAIL              : str = _("Failed to send email from '{from_user}' to '{to_user}': {error}. | category=EMAIL | action=SEND_FAIL")
    ERROR_OCCURED                     : str = _("An error occurred; email was not sent. Ensure all fields are filled. | category=EMAIL | action=ERROR")
    EMAIL_LOG_METADATA                : str = _("Recipient='{recipient}' | Subject='{subject}' | Status='{status}' | Timestamp='{timestamp}'. | category=EMAIL | action=METADATA")
    EMAIL_LOG_PAYLOAD                 : str = _("From='{from_email}' | To='{recipient}' | Subject='{subject}' | Body='{body_summary}' | Attachments={attachments}. | category=EMAIL | action=PAYLOAD")
    EMAIL_SAVED_TO_DB                 : str = _("From='{from_email}' | To='{recipient}' | Subject='{subject}' | Body='{body_summary}' has been saved to the database. | category=EMAIL | action=DATABASE_SAVE")
    EMAIL_NOT_SAVED_TO_DB             : str = _("From='{from_email}' | To='{recipient}' | Subject='{subject}' | Body='{body_summary}' was not saved to the database. | category=EMAIL | action=DATABASE_FAIL")
    START_DB_SAVE                     : str = _("Attempting to save to the database... | category=EMAIL | action=DATABASE_START")
    FAILED_TO_START_DB_SAVE           : str = _("Failed to start database save. sender='{class_name}', model='{log_model}', processed='{processed}'. | category=EMAIL | action=DATABASE_FAILED")
    MISSING_EMAIL_FIELDS              : str = _("'Subject' : {subject}, 'from_email' {from_email}, 'to_email' {to_email} | category=EMAIL | action=MISSING_FIELDS")
    
    def __str__(self) -> str:
        return _("EmailMessages: A collection of email operation-related message templates.")



# ────────────────────────────────
# TemplateResolutionMessages
# ────────────────────────────────
@dataclass(frozen=True)
class TemplateResolutionMessages(BaseFormatter):
    FOLDER_PROVIDED              : str = _("Folder provided: '{folder}'. | category=TEMPLATE | action=FOLDER_PROVIDED")
    EMAIL_DIRECTORY_PATH         : str = _("Email directory path: '{directory}'. | category=TEMPLATE | action=EMAIL_DIRECTORY_PATH")
    FULL_TEMPLATE_PATH           : str = _("Full template path resolved: '{path}'. | category=TEMPLATE | action=FULL_PATH")
    INSIDE_TEMPLATE_FOLDER_CHECK : str = _("Checking if template file is inside folder. | category=TEMPLATE | action=FOLDER_CHECK")

    def __str__(self) -> str:
        return _("TemplateResolutionMessages: A collection of template resolution-related message templates.")




# ────────────────────────────────
# FieldSummaryLog
# ────────────────────────────────
@dataclass(frozen=True)
class FieldSummaryLog:
    BEGIN_SUMMARY          : str = _("Beginning summary log... | category=SUMMARY | action=BEGIN")
    END_SUMMARY            : str = _("End of summary log. | category=SUMMARY | action=END")
    FIELDS_LOG_AND_SKIPPED : str = _("The following fields were logged '{fields}' and '{num_skipped}' were skipped. | category=SUMMARY | action=FIELDS_LOGGED_AND_SKIPPED")
    FIELDS_LOGGED          : str = _("Number of fields logged {count}. | category=SUMMARY | action=FIELDS_LOGGED")
    FIELDS_SKIPPED         : str = _("Number of fields skipped {count}, fields skipped: '{fields_skipped}'. | category=SUMMARY | action=FIELDS_SKIPPED")
    FIELDS_SUMMARY         : str = _("Optional fields are 'Context' and 'Headers'. Headers set: {headers_set}, Context set: {context_set}. | category=SUMMARY | action=FIELDS_FULL_SUMMARY")
    FIELDS_TO_SKIP         : str = _("Field '{field}' was skipped because it is in the 'do-not-log' field list. | category=SUMMARY | action=FIELD_SKIPPED")

    def __str__(self) -> str:
        return _("FieldSummaryLog: A collection of field-level summary logging messages.")



# ────────────────────────────────
# 🌍 Environment
# ────────────────────────────────
@dataclass(frozen=True)
class EnvironmentSettings:
    DEVELOPMENT: str = _("Development")
    PRODUCTION: str = _("Production")
    
    
    
# ────────────────────────────────
# Email class names
# ────────────────────────────────
@dataclass
class EmailClassNames:
    EMAILSENDER: str      = _("EmailSender")
    EMAIL_BASE_MODEL: str = _("EmailBaseLog")
    EMAIL_MODEL: str      = _("EmailLog")
    

# ────────────────────────────────
# Email Status
# ────────────────────────────────
@dataclass
class EmailStatus:
    SENT      = _("Email was successfully sent")
    NOT_SENT  = _("Email was not sent")



# ───────────────────────────────────────────────────────────────────────────────
# Email Field Status Messages
# ───────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class EmailFieldStatusMessages(BaseFormatter):
    FIELDS_NOT_SET : str = _("The field '{field}' has not been set. | category=EMAIL_FIELD | status=NOT_SET")
    FIELDS_SET     : str = _("The field '{field}' has been successfully set. | category=EMAIL_FIELD | status=SET")

    def __str__(self) -> str:
        return _("EmailFieldStatusMessages: Status messages for email field setup.")


# ───────────────────────────────────────────────────────────────────────────────
# Context and Rendering Logs
# ───────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class ContextMessages(BaseFormatter):
    RENDERING_ERROR : str = _("Error occurred during email rendering: '{error_message}'. | category=CONTEXT | status=RENDERING_ERROR")
    CONTEXT_ERROR   : str = _("Invalid context type: '{context}' (type: '{context_type}'). Expected a dictionary. | category=CONTEXT | status=INVALID_TYPE")

    def __str__(self) -> str:
        return _("ContextMessages: A collection of email context-related message templates.")


# ───────────────────────────────────────────────────────────────────────────────
# Configuration-Related Log Messages
# ───────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class ConfigMessages(BaseFormatter):
    CONFIG_NO_ACTION_TAKEN    : str = _("No action taken due to invalid or missing configuration. | category=CONFIG | status=NO_ACTION")
    CONFIG_NOT_APPLIED        : str = _("Configuration changes not applied correctly. Please check setup. | category=CONFIG | status=NOT_APPLIED")
    CONFIG_SETUP_SUCCESS      : str = _("Configuration setup completed successfully: '{config_details}'. | category=CONFIG | status=SETUP_SUCCESS")
    CONFIG_VALUE_INCORRECT    : str = _("Incorrect configuration value. Expected: '{expected_value}', got: '{actual_value}'. | category=CONFIG | status=VALUE_INCORRECT")
    INCORRECT_CONFIG_TYPE     : str = _("Invalid configuration type. Expected: '{expected_type}', got: '{actual_type}'. | category=CONFIG | status=INVALID_TYPE")
    INVALID_CONFIG_PATH       : str = _("Invalid configuration path: '{path}'. | category=CONFIG | status=INVALID_PATH")
    MISSING_CONFIG            : str = _("Missing configuration. Expected a value but got '[NONE]'. | category=CONFIG | status=MISSING")
    UNSUPPORTED_CONFIG_OPTION : str = _("Unsupported configuration option: '{option}'. | category=CONFIG | status=UNSUPPORTED_OPTION")

    def __str__(self) -> str:
        return _("ConfigMessages: Configuration-related message templates.")


# ───────────────────────────────────────────────────────────────────────────────
# Logger-Related Log Messages
# ───────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class LoggerMessages(BaseFormatter):
    """
    Logger-related log messages for the EmailSender and logging configuration.
    """
    CONFIG_LOG_LEVEL_NOT_SET         : str = _("Logger Level Not Set: Got an unexpected value for the logger. Value received: '{level}'. | category=LOGGER | status=LEVEL_NOT_SET")
    CONFIG_LOG_LEVEL_SET             : str = _("Logger Level Set: Log level set to: '{level}'. | category=LOGGER | status=LEVEL_SET")
    CONFIG_LOGGER_SETUP              : str = _("Logger Setup Complete: Logger configured successfully. | category=LOGGER | status=SETUP_COMPLETE")
    INCORRECT_CLASS_TYPE             : str = _("Incorrect Class Type: Incorrect type for '{class_name}'. Expected: '{class_name}', got: '{class_type}'. | category=LOGGER | status=INCORRECT_TYPE")
    INCORRECT_LOGTYPE                : str = _("Invalid Logger Type: Invalid logger type. Expected an instance of LoggerType, but got: '{logger_type}'. | category=LOGGER | status=INVALID_TYPE")
    LOGGER_ALREADY_INITIALISED_WARNING: str = _("Logger Initialisation Warning: Logger already initialised with level: '{level}'. Use a different config. | category=LOGGER | status=ALREADY_INITIALISED")
    LOGGER_NOT_ADDED                 : str = _("Logger Not Added: No logger found. Please add a logger before proceeding. | category=LOGGER | status=NOT_ADDED")
    LOGGER_NOT_STARTED               : str = _("Logger Not Started: Logging attempted before initialisation. Call '.start_logging_session()' first. | category=LOGGER | status=NOT_STARTED")
    LOG_LEVEL_INCORRECT_TYPE         : str = _("Invalid Log Level: Invalid log level type. Expected LoggerType, but got: '{level}'. | category=LOGGER | status=INCORRECT_LEVEL_TYPE")
    METHOD_NOT_FOUND                 : str = _("Method Not Found: Method '{method}' was not found in the class. | category=LOGGER | status=METHOD_NOT_FOUND")
    MISSING_CLASS_FIELDS             : str = _("Missing Class Fields: Missing fields in class '{class_name}'. Ensure all required fields are present. | category=LOGGER | status=MISSING_FIELDS")
    MISSING_CONFIG                   : str = _("Missing Configuration: Missing configuration. Expected values but got '[NONE]'. | category=LOGGER | status=MISSING_CONFIG")
    MISSING_LOGTYPE                  : str = _("Missing Logger Type: Logger is missing. Expected an instance of LoggerType, but got None. | category=LOGGER | status=MISSING_LOGTYPE")
    NO_ACTION_TAKEN                  : str = _("No Action Taken: No logging action was performed. | category=LOGGER | status=NO_ACTION_TAKEN")
    NOT_ENABLED                      : str = _("Logger Not Enabled: Logger is not enabled. Skipping logging. | category=LOGGER | status=NOT_ENABLED")
    SET_LOG_LEVEL_FOR_HANDLERS_MSG   : str = _("Set Handler Log Level: Handler '{handler}' log level set to: '{level}'. | category=LOGGER | status=HANDLER_LEVEL_SET")
    LEVEL_REQUEST                    : str = _("Level Change Request: User has requested a level reset to level: '{level}'. | category=LOGGER | status=LEVEL_CHANGE_REQUEST")

    def __str__(self) -> str:
        return _("LoggerMessages: Logger-related message templates for configuration and logging setup.")


# ───────────────────────────────────────────────────────────────────────────────
# Field-Related Log Messages
# ───────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class FieldMessages(BaseFormatter):
    """
    Field-related log messages for the EmailSender and field tracking system.
    Use `.format(**kwargs)` to inject dynamic values into the message template.
    """
    FIELD_ALREADY_SET          : str = _("Field '{field}' was already set to '{value}', skipping update. | category=FIELDS | status=ALREADY_SET")
    FIELD_DEFAULT_APPLIED      : str = _("Default value '{value}' applied to field '{field}'. | category=FIELDS | status=DEFAULT_APPLIED")
    FIELD_MISSING_IN_CLASS     : str = _("Field '{field}' is missing from class '{class_name}'. | category=FIELDS | status=MISSING_FIELD")
    FIELD_NOT_SET              : str = _("Field '{field}' was called but nothing was set. | category=FIELDS | status=NOT_SET")
    FIELD_SET                  : str = _("Field '{field}' was successfully set to '{value}'. | category=FIELDS | status=SET")

    def __str__(self) -> str:
        return _("FieldMessages: A collection of field-related log message templates.")


# ───────────────────────────────────────────────────────────────────────────────
# Field-Related Log Messages
# ───────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class FieldMessages(BaseFormatter):
    """
    Field-related log messages for the EmailSender and field tracking system.
    Use `.format(**kwargs)` to inject dynamic values into the message template.
    """
    FIELD_ALREADY_SET          : str = _("Field '{field}' was already set to '{value}', skipping update. | category=FIELDS | status=ALREADY_SET")
    FIELD_DEFAULT_APPLIED      : str = _("Default value '{value}' applied to field '{field}'. | category=FIELDS | status=DEFAULT_APPLIED")
    FIELD_MISSING_IN_CLASS     : str = _("Field '{field}' is missing from class '{class_name}'. | category=FIELDS | status=MISSING_FIELD")
    FIELD_NOT_SET              : str = _("Field '{field}' was called but nothing was set. | category=FIELDS | status=NOT_SET")
    FIELD_SET                  : str = _("Field '{field}' has been set with the value '{value}'. | category=FIELDS | status=SET")
    FIELD_TYPE_IS_INCORRECT    : str = _("The field type is incorrect. Expected type: '{expected_type}', but received: '{received_type}'. | category=FIELDS | status=INCORRECT_TYPE")
    FIELD_UPDATED              : str = _("Field '{field}' updated from '{old_value}' to '{new_value}'. | category=FIELDS | status=UPDATED")
    FIELD_VALIDATION_FAILED    : str = _("Validation failed for field '{field}': {reason}. | category=FIELDS | status=VALIDATION_FAILED")
    FIELD_VALIDATION_SUCCESS   : str = _("Field '{field}' passed validation. | category=FIELDS | status=VALIDATION_SUCCESS")
    FIELDS_MISSING             : str = _("An error was raised because some or all of the fields were not set. | category=FIELDS | status=MISSING_FIELDS")
    LOG_BETWEEN_FIELDS         : str = _("Field '{field_one}' to '{field_two}'. | category=FIELDS | status=FIELD_LOG")
    RECIPIENT_FIELD_ADDED_MSG  : str = _("A new email with the value '{value}' was added to the recipient list. | category=FIELDS | status=NEW_ENTRY")
    FIELD_HAS_BEEN_CLEARED     : str = _("Field '{field}' field has been 'cleared'. Field previous value was '{previous_value}', now after clearing the current value is '{value}'. | category=FIELDS | status=CLEARED")
    FIELD_CLEARING_REQUEST     : str = _("Field '{field}' field has been requested to be cleared. | category=FIELDS | status=REQUEST_CLEARING")

    def __str__(self) -> str:
        return _("FieldMessages: A collection of field-related log messages")

    def format_field_message(self, message: str, **kwargs) -> str:
        """
        Helper method to format the message string and return the translated version.
        This ensures that dynamic values are injected into the message
        before passing it to `_()` for translation.
        """
        formatted_msg = message.format(**kwargs)
        return _(formatted_msg)



# ────────────────────────────────
# Email log summary
# ────────────────────────────────
@dataclass(frozen=True)
class EmailLogSummary:
    HEADER_LINE       = _("________________________________________________________________________")
    SPACE             = _("                                                                        ")
    TITLE             = _("      '**Email Sent Process Summary Logs**'")
    SEPARATOR         = _("________________________________________________________________________")
    EMAIL_ID              = _("Email ID                          : '{email_id}'")
    TIMESTAMP             = _("Timestamp                         : {timestamp}")
    LANGUGAGE_SENT        = _("Language code sent in             : {language}")
    SUBJECT               = _("Subject                           : {subject}")
    FROM                  = _("From                              : {from_email}")
    TO                    = _("To                                : {to_email}")
    ADDITIONAL_RECIPIENTS = _("Additional Recipients             : {additional_recipients}")
    TOTAL_RECIPIENTS      = _("Total Recipients                  : {total_recipients}")
    HTML_TEMPLATE         = _("Template Used (HTML) full path    : {html_template}")
    TEXT_TEMPLATE         = _("Template Used (Text) full path    : {text_template}")
    HTML_SHORT_NAME       = _("HTML short file name              : {html_name}")
    TEXT_SHORT_NAME       = _("Text short file name              : {text_name}")
    ATTACHMENTS           = _("Attachments Added                 : '{attachments}'")
    ENVIRONMENT           = _("Environment                       : '{environment}'")
    TIME_TAKEN            = _("Time Taken                        : {time_taken:.2f} seconds")
    STATUS                = _("Status                            : {status_message}")
    DELIVERED             = _("Emails delivered successfully     : {delivered}")
    TEXT_PREVIEW          = _("Text Preview                      : {text_preview}")
    HTML_PREVIEW          = _("HTML Preview                      : {html_preview}")
    EMAIL_FORMAT          = _("Email format                      : multipart/alternative (HTML + plain text)")
    BOTTOM_LINE           = _("________________________________________________________________________")

    @staticmethod
    def format_email_log_summary(message: str, **kwargs) -> str:
        """
        Helper method to format the message string and return the translated version.
        This ensures that dynamic values are injected into the message
        before passing it to `_()` for translation.
        """
        formatted_msg = message.format(**kwargs)
        return _(formatted_msg)



# ────────────────────────────────
# MethodConstants
# ────────────────────────────────
@dataclass(frozen=True)
class MethodConstants(BaseFormatter):
    """
    Method-related log messages for the EmailSender and method tracking system.
    Use `.format(**kwargs)` to inject dynamic values into the message template.
    """
    EVALUATING_FIELD_METHODS     : str = _("Evaluating field methods for class '{class_name}'. | category=METHOD | status=EVALUATING")
    EXCEPTION_ERRORS             : str = _("The method '{method}' returned an invalid field value: '{field}'. | category=METHOD | status=VALUE_ERROR")
    INVALID_EMAIL_INSTANCE       : str = _("Invalid email instance provided. | category=METHOD | status=INVALID_INSTANCE")
    METHOD_FIELD_SIGNATURE_CHECK : str = _("Checking __init__ field '{field}' in class '{class_name}'. Field present: '{has_field}'. | category=METHOD | status=CHECKING_FIELDS")
    METHOD_PARAMS_CHECK          : str = _("Checking parameters of method '{method}' in class '{class_name}' against: {params}. | category=METHOD | status=CHECKING_PARAMS")
    METHOD_SIGNATURE_CHECK       : str = _("Checking method signature for field '{field}' in class '{class_name}'. Valid: '{has_field}'. | category=METHOD | status=CHECKING_SIGNATURE")
    MISSING_FIELDS_ERROR         : str = _("Required items missing. Fields: {fields}, Methods: {methods}. | category=METHOD | status=MISSING_FIELDS")
    MISSING_CLASS_FIELDS         : str = _("The following fields or methods are missing: Fields: {fields}, Methods: {methods}")

    def __str__(self) -> str:
        return _("MethodConstants: A collection of method-related log messages.")



# ────────────────────────────────
# Recipient messges
# ────────────────────────────────
@dataclass(frozen=True)
class RecipientMessages(BaseFormatter):
    """
    Log messages related to recipient handling for the EmailSender.
    """
    RECIPIENT_ADDED_TO_LIST     : str = _("Email added to the recipient list: '{recipient}'. | category=RECIPIENT | status=ADDED")
    RECIPIENT_REMOVED_FROM_LIST : str = _("Email removed from the recipient list: '{recipient}'. | category=RECIPIENT | status=REMOVED")
    RECIPIENT_LIST_CLEARED      : str = _("All recipients cleared from the list. | category=RECIPIENT | status=CLEARED")

    def __str__(self) -> str:
        return _("RecipientMessages: A collection of recipient-related log message templates.")



# ────────────────────────────────
# AuditTrail Messages
# ────────────────────────────────
@dataclass(frozen=True)
class AuditTrailMessages(BaseFormatter):
    """
    Log messages related to audit trail updates.
    """
    AUDIT_TRAIL_UPDATED : str = _("Audit trail successfully updated. | category=AUDIT_TRAIL | status=UPDATED")
    FIELD_CHANGED       : str = _("Field changed. Audit trail will be updated. | category=AUDIT_TRAIL | status=FIELD_CHANGED")
    SHOW_AUDIT_TRAIL    : str = _("Displaying audit trail: {audit_trail}. | category=AUDIT_TRAIL | status=SHOW")

    def __str__(self) -> str:
        return _("AuditTrailMessages: A collection of audit trail-related log message templates.")



# ────────────────────────────────
# Log Execution messages
# ────────────────────────────────
@dataclass(frozen=True)
class LogExecutionMessages(BaseFormatter):
    """
    Runtime logging messages related to execution flow, tracing, and diagnostics.
    """
    TRACE_FORMAT_FUNCTION_CALLED: str = _("Calling function: {function_name}() | category=LOG | status=TRACE")
    VERBOSE_ATTEMPT_RETRIEVE    : str = _("Attempting to retrieve HTML and text file paths. | category=LOG | status=VERBOSE")
    VERBOSE_RETRIEVE_FAILED     : str = _("Failed to retrieve file paths. HTML: {html}, Text: {text}. | category=LOG | status=FAILED")
    VERBOSE_RETRIEVE_SUCCESS    : str = _("Successfully retrieved HTML: {html} and TEXT: {text} file paths. | category=LOG | status=SUCCESS")
    FALLBACK_TEMPLATE_USED      : str = _("No valid template found. Using fallback template: {template_name}. | category=LOG | status=FALLBACK")
    FILE_PATH_NOT_FOUND        : str = _("File path not found for template type: {template_type}. | category=LOG | status=WARNING")

    def __str__(self) -> str:
        return _("LogExecutionMessages: Templates for structured trace and execution log messages.")


# ────────────────────────────────
# Debug messages
# ────────────────────────────────
@dataclass(frozen=True)
class DebugMessages(BaseFormatter):
    """
    Structured debug log messages used for tracing and diagnostic purposes.
    Use `.format(**kwargs)` to inject dynamic values into each template.
    """
    DEBUG_SESSION_CONCLUDED   : str = _("Debug session concluded at method '{current_method}'. | category=DEBUG | status=SESSION_CONCLUDED")
    DEBUG_SESSION_STARTED     : str = _("Debug session started at method '{current_method}'. | category=DEBUG | status=SESSION_STARTED")
    METHOD_ENDED_DEBUG        : str = _("Debugging ended at method '{current_method}'. | category=DEBUG | status=METHOD_ENDED")
    METHOD_SKIPPED_DEBUG      : str = _("Method '{current_method}' skipped from debugging due to the 'do-not-debug' list. | category=DEBUG | status=METHOD_SKIPPED")
    METHOD_STARTED_DEBUG      : str = _("Debugging enabled for method '{current_method}'. | category=DEBUG | status=METHOD_STARTED")
    VERBOSE_TRACE             : str = _("'Debug trace:' entered '{class_name}.{current_method}' at line {line_number} in class '{class_name}'. | category=DEBUG | status=TRACE")
    VERBOSE_TRACE_ENTERED     : str = _("Entered trace depth level {depth_level}. | category=DEBUG | status=TRACE_LEVEL")
    METHOD_CHAIN_TRACE        : str = _("Method Chain Started: {method_trace} | category=DEBUG | status=METHOD_TRACE")

    @staticmethod
    def format_debug_log_message(message: str, **kwargs) -> str:
        """
        Helper method to format the message string and return the formatted version.
        """
        try:
            return message.format(**kwargs)
        except (IndexError, KeyError):
            return message
    
