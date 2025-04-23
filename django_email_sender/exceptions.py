class EmailSenderError(Exception):
    """Base exception for all email sender errors."""
    pass


class EmailTemplateDirNotFound(EmailSenderError):
    """Raised when the email_templates directory is not found."""
    pass


class EmailTemplateNotFound(EmailSenderError):
    """Raised when a specific email template file is missing."""
    pass


class TemplateDirNotFound(EmailSenderError):
    """Raised when a template directory does not exist."""
    pass
