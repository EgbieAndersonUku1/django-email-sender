import json
from datetime import datetime

from django.test import TestCase
from django.core import mail
from unittest.mock import Mock, patch
from django.utils import timezone

from django_email_sender.email_sender import EmailSender
from django_email_sender.email_sender_payload import EmailPayload, EmailMetaData
from django_email_sender.exceptions import EmailSenderBaseException
from .test_fixture import (EmailSenderConstants,
                           create_email_logger_instance, 
                           TEMPLATES_DIR,
                           create_template_path)

from django_email_sender.messages import EmailStatus


TEXT_CONTENT = "text_content"
HTML_CONTENT = "html_content"


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
        self.assertEqual(mail.outbox[0].body, TEXT_CONTENT, msg="Expected the to email the match the body")
    
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


    def tearDown(self):
        self.email_sender = None



class EmailSenderLoggerSendTest(TestCase):
    
    def setUp(self):  
        self.email_sender_logger = create_email_logger_instance(EmailSenderConstants, EmailSender.create())

    @patch("django_email_sender.email_sender.render_to_string")
    def _send_email_helper(self, mock_render_string):
 
        # Mock template rendering: first call returns text content, second call returns HTML content
        mock_render_string.side_effect = [TEXT_CONTENT, HTML_CONTENT]
   
        # Mock `_validate` to bypass validation logic during this test
        with patch.object(EmailSender, '_validate', return_value=None):
            self.email_sender_logger.send()
                        
    def test_send(self):
        
        self._send_email_helper()
        
        # Validate that one email was sent
        self.assertEqual(len(mail.outbox), 1)     

        # The tests below verifiy if the fields match the expected fields e.g subject, body, etc
        self.assertEqual( mail.outbox[0].subject, EmailSenderConstants.subject, msg="Expected the subject to match the one sent")

        self.assertEqual(mail.outbox[0].to,
            [self.email_sender_logger._email_sender.to_email],
            msg="Expected the 'to' email to match the recipients sent"
        )
        
        self.assertEqual(
            mail.outbox[0].body,
            TEXT_CONTENT,
            msg="Expected the plain text body to match the rendered content"
        )

        # check that processed email flag was set
        self.assertTrue(self.email_sender_logger._email_was_processed)
        
    def test_successful_email_send_returns_payload(self):

         # Assert that when no email has been sent the payload isis None
        self.assertIsNone(self.email_sender_logger.return_successful_payload())
         
        self._send_email_helper()

        payload = self.email_sender_logger.return_successful_payload()
        self.assertIsNotNone(payload)

        # Build the expected payload for comparison
        html_template = create_template_path(EmailSenderConstants.html_template, email_templates_dir=TEMPLATES_DIR)
        text_template = create_template_path(EmailSenderConstants.text_template, email_templates_dir=TEMPLATES_DIR)

        expected_payload = EmailPayload(
            to_email=EmailSenderConstants.to_email,
            from_email=EmailSenderConstants.from_email,
            subject=EmailSenderConstants.subject,
            body_html=html_template,
            body_text=text_template,
            context=EmailSenderConstants.context,
            headers=EmailSenderConstants.headers,
        )

        self.assertEqual(payload, expected_payload.to_json())
        
    def test_successful_email_send_returns_correct_metadata(self):
        
        self.assertFalse(self.email_sender_logger.email_meta_data)
        self._send_email_helper()

        self.assertTrue(self.email_sender_logger.email_meta_data)

        # Build expected metadata (except for timestamp, which is dynamic)
        expected_meta_data = EmailMetaData(
            to_email=EmailSenderConstants.to_email,
            subject=EmailSenderConstants.subject,
            status=self.email_sender_logger._was_sent_successfully,
            timestamp=None, # set to None since it is not used as part of the meta checking
            errors=False,
        )

        # Deserialize the metadata for comparison
        email_sender_meta_data = json.loads(self.email_sender_logger.email_meta_data)
     
        # The metadata must be compared field-by-field rather than directly like the payload
        # where it was compared like this `self.assertEqual(payload, expected_payload.to_json())`.
        # This is because the 'timestamp' field is generated dynamically after sending the email,
        # making a full-object comparison unreliable.
        is_email_sent = EmailStatus.SENT if expected_meta_data.status else EmailStatus.NOT_SENT

        self.assertEqual(expected_meta_data.to_email, email_sender_meta_data["to_email"])
        self.assertEqual(expected_meta_data.subject, email_sender_meta_data["subject"])
        self.assertEqual(is_email_sent, email_sender_meta_data["status"])

        # Ensure the recorded timestamp is less than current timestamp
        self.assertLessEqual(
            datetime.fromisoformat(email_sender_meta_data["timestamp"]),
            timezone.now()
        )

    def test_email_sent_property(self):
        """
        Test that the `is_email_sent` property correctly reflects email sending status.

        Initially, the property should be False. After sending an email using the helper 
        method, it should be True.
        """
        self.assertFalse(self.email_sender_logger.is_email_sent)

        # send an email
        self._send_email_helper()
        
        # check that an boolean flag of True is returned after an email is sent
        self.assertTrue(self.email_sender_logger.is_email_sent)

    def test_email_delivery_count(self):
        """
        Test that `email_delivery_count` increments correctly when emails are sent.

        Verifies that the count starts at 0, increments by one after each email sent 
        using the helper method.
        """
        
        # test that before an email is sent the count is 0
        self.assertEqual(self.email_sender_logger.email_delivery_count, 0)
        
        # send an email
        self._send_email_helper()
        
        # Test that email count is now 1
        self.assertEqual(self.email_sender_logger.email_delivery_count, 1)
                
        self._send_email_helper()
        
        # Test that email count is now 2
        self.assertEqual(self.email_sender_logger.email_delivery_count, 2)
    
    def tearDown(self):
        self.email_sender_logger = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
   