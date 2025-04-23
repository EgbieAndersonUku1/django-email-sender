from typing import Optional, List, Dict, Union
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pathlib import Path
from os.path import join, exists

from django_email_sender.exceptions import EmailTemplateDirNotFound, EmailTemplateNotFound, TemplateDirNotFound, EmailSenderError

from .utils import get_template_dirs

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dirs                 = get_template_dirs()
TEMPLATES_DIR        = dirs["TEMPLATES_DIR"]
EMAIL_TEMPLATES_DIR  = dirs["EMAIL_TEMPLATES_DIR"]



class EmailSender:
    """
    An email sender that allows you to send emails by
    using a chaining method. This is mostly to be used in
    the Django eco-system.

    To use it in a Django eco-system, the following settings must be configured:

    settings.py:
    EMAIL_USE_TLS = True  
    EMAIL_HOST = 'smtp.gmail.com'  
    EMAIL_PORT = 587  
    EMAIL_HOST_USER = 'some@emailhere.com'  
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
        self.to_email: List[str]          = []
        self.subject: Optional[str]       = None
        self.html_template: Optional[str] = None
        self.text_template: Optional[str] = None
        self.context: Dict                = {}
        self.headers: Dict                = {}

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
        self.from_email = email
        return self

    def to(self, recipients: Union[str, List[str]]) -> "EmailSender":
        """
        Set the recipient(s) of the email.

        If a single email is provided as a string, it converts it into a list.
        Otherwise, it assumes a list of email addresses.
        
        Args:
            recipients (Union[str, List[str]]): A single email address or a list of email addresses.
            

        Returns:
            EmailSender: The current instance for chaining.
        """
        self.to_email = [recipients] if isinstance(recipients, str) else recipients
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

    def _does_template_path_exists(self, email_path):
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
           raise TemplateDirNotFound(f"The templates directory wasn't found. Got template with path - {TEMPLATES_DIR}")
        if not exists(EMAIL_TEMPLATES_DIR):
           raise EmailTemplateDirNotFound(f"The emails_templates directory wasn't found. Got path - {EMAIL_TEMPLATES_DIR}")
        if not exists(email_path):
            raise EmailTemplateNotFound(f"The email template path wasn't found. Got email path - {email_path}")
    
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

        if folder_name != None and not isinstance(folder_name, str):
            raise ValueError("The folder name must be a string or None")
        if not isinstance(template_name, str):
            raise ValueError("The template name must be a string or None")
        
        if folder_name is None:
            return join(EMAIL_TEMPLATES_DIR, template_name)
        return join(EMAIL_TEMPLATES_DIR, folder_name, template_name)
            

    def with_headers(self, headers: Optional[Dict] = None) -> "EmailSender":
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
            raise TypeError(f"Headers must be a dictionary, got {type(headers)} instead.")
        self.headers = headers
        return self

    def send(self) -> int:
        """
        Send the email using Django's email backend.

        This will render the text and HTML templates, attach the HTML alternative, and send the email.

        Raises:
            ValueError: If any required fields are missing before sending.
            EmailSendError: Raises an EmailSendError if an error occurs while sending an email.

        Returns:
            int: The number of successfully delivered messages (typically 1 if successful).
        """
        if not all([self.from_email, self.to_email, self.subject, self.html_template, self.text_template]):
            raise ValueError("All email components (from, to, subject, html, text) must be set before sending.")

        self._does_template_path_exists(self.text_template)
        self._does_template_path_exists(self.html_template)
        
        text_content = render_to_string(self.text_template, context=self.context)
        html_content = render_to_string(self.html_template, context=self.context)

        msg = EmailMultiAlternatives(
            subject=self.subject,
            body=text_content,
            from_email=self.from_email,
            to=self.to_email,
            headers=self.headers or None
        )

        msg.attach_alternative(html_content, "text/html")
        
        try:
            return msg.send()
        except EmailSenderError as e:
            raise EmailSenderError(str(e))
