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
    pass
  
class EmailSendError(BaseException):
    """Raised when an error occurs during sending an email"""
    
        
class EmailNotSetError(BaseException):
    """Raised when an email is not sent."""
    pass

class TemplateDirNotFound(BaseException):
    """Exception raised when the template directory does not exist."""
    pass
   

class EmailTemplateNotFound(BaseException):
    """Raised when a specific email template file is missing."""
    pass
    
    
class TemplateNotFound(BaseException):
    """Exception raised when a specific template file is missing."""
    pass

    
class ContextIsNotADictionary(BaseException):
    """Raised when the context is not a dictionary"""
    pass

class ResetFieldsAttribruteError(BaseException):
    """Raised when the attribute of EmailSender is not found"""
    pass

class LoggerTypeError(BaseException):
    """Raised when an incorrect logger type is passed to EmailSender"""
    pass


class LoggerNotStartedError(BaseException):
    """Raised when the logger hasn't been startedr"""
    pass


class InvalidPayload(BaseException):
    """Raised when an invalid payload occurs"""
    pass


class InvalidMetadata(BaseException):
    """Raised when an invalid payload occurs"""
    pass

class LoggerNotAddedError(BaseException):
    """Raised when the logger hasn't been startedr"""
    pass


class IncorrectEmailSenderInstance(BaseException):
    """Raised when an incorrect email instance is added"""
    pass


class IncorrectLoggerLevelSettings(BaseException):
    """Raised when an incorrect email instance is added"""
    pass


class IncorrectEmailSenderFieldType(BaseException):
    """Raised when an incorrect email field type is added"""
    pass


class MissingFieldsInClass(BaseException):
    """Raised when a class contains missing fields"""
    pass


class IncorrectEmailModelAddedError(BaseException):
    pass

class MethodNotFoundError(EmailSenderBaseException):
    """Raised when a method is not found in a given class"""
    pass
        
class LoggerBaseException(EmailSenderBaseException):
    """"BaseException class that raised Errors"""
    pass
        
    