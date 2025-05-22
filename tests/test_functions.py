from django.test import TestCase
from unittest.mock import Mock, patch

from django_email_sender.email_sender import EmailSender
from django_email_sender.utils import (get_safe_text_preview,
                                       get_html_preview,
                                       measure_duration,
                                       sanitize_for_json,
                                       )

from .test_fixture import (EmailSenderConstants, 
                           create_email_sender_instance,
                           create_email_logger_instance, 
                           )


class TestEmailSender(TestCase):

    def setUp(self):  
        self.email_sender_logger = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
    
    @patch("django_email_sender.email_sender.render_to_string")
    def test_measure_time_send_function(self, mock_render_string, *args, **kwargs):
        """
        Tests the `measure_duration` function, which measures the time taken to send an email.

        Note:
        This test does not actually send an email, and the required template files 
        (e.g., HTML and plain text) do not exist. Therefore, the Django `render_to_string` 
        function and the `validate` method of `EmailSenderLogger` are mocked to prevent 
        errors during the test.
        """
 
        # check that email count is 0 before the email is sent.
        self.assertEqual(self.email_sender_logger.email_delivery_count, 0)
             
        TEXT_CONTENT = "text body"
        HTML_CONTENT = "html body"
        
        # Mock template rendering: first call returns text content, second call returns HTML content
        mock_render_string.side_effect = [TEXT_CONTENT, HTML_CONTENT]
   
        # Mock `_validate` to bypass validation logic during this test
        with patch.object(EmailSender, '_validate', return_value=None):      
            email_resp, elasped = measure_duration(self.email_sender_logger._email_sender.send, *args, **kwargs)
      
        
        self.assertTrue(email_resp)
        self.assertTrue(elasped)
        
        emails_sent_count, is_sent = email_resp
        
        self.assertEqual(emails_sent_count, 1)
        self.assertTrue(is_sent)
        
        self.assertIsInstance(elasped, float)
      