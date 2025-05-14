from django.test import TestCase
from django.core import mail
from unittest.mock import Mock, patch

from django_email_sender.email_sender import EmailSender

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
        
        # Verify recipient list
        self.assertEqual(mail.outbox[0].body, TEXT_CONTENT, msg="Expected the to email the match the headers")