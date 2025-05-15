from django.test import TestCase
from django.core import mail
from unittest.mock import Mock, patch

from django_email_sender.email_sender import EmailSender
from django_email_sender.exceptions import EmailSenderBaseException
from .test_fixture import EmailSenderConstants




class EmailSenderSendTest(TestCase):
    
    def setUp(self):  
        self.from_email     = "no-reply@example.com"
        self.to_email       = "to-reply@example.com"
        self.subject        = "test subject"
        self.context        = {"code": "1234"}
        self.headers        = {"headers": "1234"}
        self.html_template  = "test.html"
        self.text_template  = "test.txt"
        
        self.email_sender   =  EmailSender.create()

        (
            self.email_sender
            .from_address(self.from_email)
            .to(self.to_email)
            .with_subject(self.subject)
            .with_context(self.context)
            .with_headers(self.headers)
            .with_html_template(self.html_template)
            .with_text_template(self.text_template)
        )
        
    @patch("django_email_sender.email_sender.render_to_string")
    def test_send(self, mock_render_string):
        
        TEXT_CONTENT = "text_content"
        HTML_CONTENT = "html_content"
        
        mock_render_string.side_effect = [
            TEXT_CONTENT,  
            HTML_CONTENT,   
        ]
        
        email_sender = EmailSender()
        (
            email_sender
            .from_address(self.from_email)
            .to(self.to_email)
            .with_subject(self.subject)
            .with_context(self.context)
            .with_headers(self.headers)
            .with_html_template(self.html_template)
            .with_text_template(self.text_template)
        )
        with patch.object(EmailSender, '_validate', return_value=None):
            email_sender.send()
           
        # Validate that one email was sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Validate the subject sent matches the subject
        self.assertEqual(mail.outbox[0].subject, self.subject, msg="Expected the subject to match the one sent")
        
        # Verify recipient list
        self.assertEqual(mail.outbox[0].to, [self.email_sender.to_email], msg="Expected the to email the match the recipients sent")
        
        # Verify the body
        self.assertEqual(mail.outbox[0].body, TEXT_CONTENT, msg="Expected the to email the match the headers")
    
    @patch("django_email_sender.email_sender.render_to_string")
    def test_send_raises_error_when_from_email_is_missing(self, mock_render_string):
        """
        Ensures an EmailSenderBaseException is raised when 'from_email' is missing.
        """
        mock_render_string.side_effect = ["text_content", "html_content"]
        email_sender = creating_instance_with_missing_fields(from_email=None)

        EXPECTED_ERROR = (
            "[EmailSenderBaseException] All email components (from, to, subject, html, text) "
            "must be set before sending."
        )

        with self.assertRaises(EmailSenderBaseException) as cm:
            email_sender.send()

        self.assertIsInstance(cm.exception, EmailSenderBaseException)
        self.assertEqual(str(cm.exception), EXPECTED_ERROR)


    @patch("django_email_sender.email_sender.render_to_string")
    def test_send_raises_error_when_to_email_is_missing(self, mock_render_string):
        """
        Ensures an EmailSenderBaseException is raised when 'to_email' is missing.
        """
        mock_render_string.side_effect = ["text_content", "html_content"]
        email_sender = creating_instance_with_missing_fields(to_email=None)

        EXPECTED_ERROR = (
            "[EmailSenderBaseException] All email components (from, to, subject, html, text) "
            "must be set before sending."
        )

        with self.assertRaises(EmailSenderBaseException) as cm:
            email_sender.send()

        self.assertIsInstance(cm.exception, EmailSenderBaseException)
        self.assertEqual(str(cm.exception), EXPECTED_ERROR)


    @patch("django_email_sender.email_sender.render_to_string")
    def test_send_raises_error_when_subject_is_missing(self, mock_render_string):
        """
        Ensures an EmailSenderBaseException is raised when 'subject' is missing.
        """
        mock_render_string.side_effect = ["text_content", "html_content"]
        email_sender = creating_instance_with_missing_fields(subject=None)

        EXPECTED_ERROR = (
            "[EmailSenderBaseException] All email components (from, to, subject, html, text) "
            "must be set before sending."
        )

        with self.assertRaises(EmailSenderBaseException) as cm:
            email_sender.send()

        self.assertIsInstance(cm.exception, EmailSenderBaseException)
        self.assertEqual(str(cm.exception), EXPECTED_ERROR)




def creating_instance_with_missing_fields(from_email: str    = EmailSenderConstants.from_email,
                                          to_email: str      = EmailSenderConstants.to_email,
                                          subject: str       = EmailSenderConstants.subject,
                                          context: dict      = EmailSenderConstants.context,
                                          headers: dict      = EmailSenderConstants.headers,
                                          html_template: str = EmailSenderConstants.html_template,
                                          text_template: str = EmailSenderConstants.text_template, 
                                          ):

    email_sender = EmailSender.create()
    (
            email_sender
            .from_address(from_email)
            .to(to_email)
            .with_subject(subject)
            .with_context(context)
            .with_headers(headers)
            .with_html_template(html_template)
            .with_text_template(text_template)
    )
        
    return email_sender