from django_email_sender.utils import get_template_dirs
from django_email_sender.email_sender import EmailSender
from django_email_sender.email_logger import EmailSenderLogger
from os.path import join

dirs                = get_template_dirs()
TEMPLATES_DIR       = dirs["TEMPLATES_DIR"]
EMAIL_TEMPLATES_DIR = dirs["EMAIL_TEMPLATES_DIR"]


class EmailSenderConstants:
    from_email     = "no-reply@example.com"
    to_email       = "to-reply@example.com"
    subject        = "test subject"
    context        = {"code": "1234"}
    headers        = {"headers": "1234"}
    html_template  = "test.html"
    text_template  = "test.txt"
    
    
def create_email_sender_instance(email_sender_constants_class):
    email_sender =  EmailSender.create()

    (
        email_sender
        .from_address(email_sender_constants_class.from_email)
        .to(email_sender_constants_class.to_email)
        .with_subject(email_sender_constants_class.subject)
        .with_context(email_sender_constants_class.context)
        .with_headers(email_sender_constants_class.headers)
        .with_html_template(email_sender_constants_class.html_template)
        .with_text_template(email_sender_constants_class.text_template)
    )
    
    return email_sender


def create_template_path(template: str, email_templates_dir: str = EMAIL_TEMPLATES_DIR) -> str:
    """
    Constructs the full path to an email template by joining the given 
    template name with the email templates directory.

    Note:
        This function does not check whether the resulting path exists; it 
        simply joins the directory and template name.

    Args:
        template (str): The name of the template file, including its extension 
            (e.g., "welcome_email.html").
        email_templates_dir (str): The path to the directory containing templates 
            (e.g., "templates/email"). Defaults to EMAIL_TEMPLATES_DIR.

    Returns:
        str: The full path to the specified template.
    """
    return join(email_templates_dir, template)


def test_missing_template(self, missing_template_path, exception_error):
    """
    Test if a template not found error is raises if it does cont
    """
   
    email_sender    = create_email_sender_instance(EmailSenderConstants)
    html_template   = create_template_path(EmailSenderConstants.text_template, email_templates_dir=missing_template_path)
    text_template   = create_template_path(EmailSenderConstants.html_template, email_templates_dir=missing_template_path)
        
    EmailSenderConstants.html_template = html_template
    EmailSenderConstants.text_template  = text_template
    
    with self.assertRaises(TemplateDirNotFound) as custom_message:
        email_sender.send()

    exc = custom_message.exception
    self.assertIsInstance(exc, TemplateDirNotFound)
    self.assertEqual(str(exc), exception_error)



def create_email_logger_instance(email_sender_constants_class, email_sender_instance):
    email_sender_logger = EmailSenderLogger.create()
     
    ( email_sender_logger
      .add_email_sender_instance(email_sender_instance)
      .from_address(email_sender_constants_class.from_email)
      .to(email_sender_constants_class.to_email)
      .with_context(email_sender_constants_class.context)
      .with_subject(email_sender_constants_class.subject)
      .with_headers(email_sender_constants_class.headers)
      .with_html_template(email_sender_constants_class.html_template)
      .with_text_template(email_sender_constants_class.text_template)        
    )
    return email_sender_logger


