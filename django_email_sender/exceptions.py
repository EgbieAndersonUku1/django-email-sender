from django.utils.translation import gettext_lazy as _


class BaseException(Exception):
    """Base exception for all email sender errors with formatting and optional translation."""

    def __init__(self, message=None, *args, **kwargs):
        self.original_message = message
        self.format_args = args
        self.format_kwargs = kwargs

        formatted_message = self._format_message(message, *args, **kwargs)
        super().__init__(formatted_message)

    @staticmethod
    def _format_message(message, *args, **kwargs):
        """Format the already-translated message."""
        if message:
            try:
                return message.format(*args, **kwargs)
            except Exception as e:
                return message
        return _("An unknown error occurred")

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.args[0]}"

    def debug_info(self):
        """Optional method to expose full debug context."""
        return {
            "exception": self.__class__.__name__,
            "original_message": str(self.original_message),
            "format_args": [str(arg) for arg in self.format_args],
            "format_kwargs": {k: str(v) for k, v in self.format_kwargs.items()},
            "formatted_message": str(self),
        }




class EmailSenderBaseException(BaseException):
    """Base exception for EmailSender errors."""
  

class EmailSendError(BaseException):
    """Raised when an error occurs during sending an email"""


class EmailNotSetError(BaseException):
    """Raised when an email is not sent."""


class TemplateDirNotFound(BaseException):
    """Exception raised when the template directory does not exist."""



class EmailTemplateNotFound(BaseException):
    """Raised when a specific email template file is missing."""



class TemplateNotFound(BaseException):
    """Exception raised when a specific template file is missing."""



class ContextIsNotADictionary(BaseException):
    """Raised when the context is not a dictionary"""


class ResetFieldsAttribruteError(BaseException):
    """Raised when the attribute of EmailSender is not found"""


class LoggerTypeError(BaseException):
    """Raised when an incorrect logger type is passed to EmailSender"""



class LoggerNotStartedError(BaseException):
    """Raised when the logger hasn't been startedr"""



class InvalidPayload(BaseException):
    """Raised when an invalid payload occurs"""


class InvalidMetadata(BaseException):
    """Raised when an invalid payload occurs"""


class LoggerNotAddedError(BaseException):
    """Raised when the logger hasn't been startedr"""


class IncorrectEmailSenderInstance(BaseException):
    """Raised when an incorrect email instance is added"""



class IncorrectLoggerLevelSettings(BaseException):
    """Raised when an incorrect email instance is added"""



class IncorrectEmailSenderFieldType(BaseException):
    """Raised when an incorrect email field type is added"""


class MissingFieldsInClass(BaseException):
    """Raised when a class contains missing fields"""



class IncorrectEmailModelAddedError(BaseException):
    """Raised when an incorrect email model is added"""

class MethodNotFoundError(EmailSenderBaseException):
    """Raised when a method is not found in a given class"""


class LoggerBaseException(EmailSenderBaseException):
    """"BaseException class that raised Errors"""


class InvalidIdempotencyKey(EmailSenderBaseException):
    """Raised when an invalid Idempotency key is passed"""
