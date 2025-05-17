from django.test import TestCase

from django_email_sender.email_sender import EmailSender
from django_email_sender.exceptions import TemplateDirNotFound, IncorrectEmailSenderInstance
from .test_fixture import (EmailSenderConstants, 
                           create_email_sender_instance,
                           create_template_path,
                           test_missing_template,
                           TEMPLATES_DIR,
                           EMAIL_TEMPLATES_DIR,
                           create_email_logger_instance,
                           
                           )

class EmailSenderLoggerTest(TestCase):
    
    def setUp(self):  
        self.email_sender_logger = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
    
    def test_email_logger_is_created(self):
        self.assertTrue(self.email_sender_logger)
    
    def test_fields(self):
        html_path = create_template_path(EmailSenderConstants.html_template)
        text_path = create_template_path(EmailSenderConstants.text_template)
        
        # test if the fields were actually assigned to the email
        self.assertEqual(self.email_sender_logger._email_sender.from_email, EmailSenderConstants.from_email)
        self.assertEqual(self.email_sender_logger._email_sender.to_email, EmailSenderConstants.to_email)
        self.assertEqual(self.email_sender_logger._email_sender.subject,  EmailSenderConstants.subject)
        self.assertEqual(self.email_sender_logger._email_sender.context,  EmailSenderConstants.context)
        self.assertEqual(self.email_sender_logger._email_sender.headers,  EmailSenderConstants.headers)
        self.assertEqual(self.email_sender_logger._email_sender.html_template, html_path)
        self.assertEqual(self.email_sender_logger._email_sender.text_template, text_path)
    
    def test_raises_error_when_invalid_email_sender_instance_provided(self):
      
        class IncorrectEmailSender:
           pass
          
           @classmethod
           def create(cls):
               return cls()
        
        with self.assertRaises(IncorrectEmailSenderInstance) as custom_message:
            
            create_email_logger_instance(EmailSenderConstants, IncorrectEmailSender.create())
        
        self.assertIsInstance(custom_message.exception, IncorrectEmailSenderInstance)
          
    def test_clear_from_email_method(self):
        """
        Verifies that when the ".clear_from_email()" method is called on the "EmailSender"
        class instance then the "from_email" field is cleared.
        """
        self.assertTrue(self.email_sender_logger._email_sender.from_email)
        self.email_sender_logger.clear_from_email()
        self.assertIsNone(self.email_sender_logger._email_sender.from_email)
        
    def test_clear_from_email_method(self):
        """
        Verifies that when the ".clear_to_email()" method is called on the "EmailSender"
        class instance then the "to_email" field is cleared.
        """
        self.assertTrue(self.email_sender_logger._email_sender.to_email)
        self.email_sender_logger.clear_to_email()
        self.assertFalse(self.email_sender_logger._email_sender.to_email)
    
    def test_clear_subject_method(self):
        """
        Verifies that when the ".clear_subject()" method is called on the "EmailSender"
        class instance then the "subject" field is cleared.
        """
        self.assertTrue(self.email_sender_logger._email_sender.subject)
        self.email_sender_logger.clear_subject()
        self.assertIsNone(self.email_sender_logger._email_sender.subject)
    
    def test_clear_context_method(self):
        """
        Verifies that when the ".clear_context()" method is called on the "EmailSender"
        class instance then the "context" field is cleared.
        """
        self.assertTrue(self.email_sender_logger._email_sender.context)
        self.email_sender_logger.clear_context()
        self.assertFalse(self.email_sender_logger._email_sender.context)
        self.assertIsInstance(self.email_sender_logger._email_sender.context, dict)
              
    def clear_all_fields(self):
        """
        Verifies that when the ".clear_all_fields()" method is called on the "EmailSender"
        class instance then the all the fields are cleared.
        
        The fields that are cleared are:
            - from_email
            - to_email
            - subject
            - context
            - headers
            - html_template
            - text_template
        """
        email_sender =  EmailSender.create()

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
        
        html_path = join(EMAIL_TEMPLATES_DIR, self.html_template)
        text_path = join(EMAIL_TEMPLATES_DIR, self.text_template)
        
        # Assert that the fields are not empty
        self.assertEqual(self._email_sender_logger._email_sender.from_email, self.from_email)
        self.assertEqual(self._email_sender_logger._email_sender.to_email, self.to_email)
        self.assertEqual(self._email_sender_logger._email_sender.subject, self.subject)
        self.assertEqual(self._email_sender_logger._email_sender.context, self.context)
        self.assertEqual(self._email_sender_logger._email_sender.headers, self.headers)
        
        self.assertEqual(self._email_sender_logger._email_sender.html_template, html_path)
        self.assertEqual(self._email_sender_logger._email_sender.text_template, text_path)
        
        
        email_sender.clear_all_fields()
        
        # assert that all fiels are now empty after clearing
        self.assertFalse(email_sender.from_email)
        self.assertFalse(email_sender.to_email)
        self.assertFalse(email_sender.subject)
        self.assertFalse(email_sender.context)
        self.assertFalse(email_sender.headers)
        self.assertFalse(email_sender.html_template)
        self.assertFalse(email_sender.text_template)
    
    def test_add_new_recipient_method(self):
        """
        Ensures that when the `.add_new_recipient()` method is called,
        a new recipient email is added to the list of recipients to 
        send an email to. The `EmailSenderLogger` actually calls
        the `EmailSender` method behind the scene because it doesn't 
        actually store he names inside its object
        """
        TEST_EMAIL    = "test@example.com"
        TEST_EMAIL_2  = "test2@example.com"
        
        # access it through the '_email_sender'
        email_logger = self.email_sender_logger._email_sender
        
        self.assertFalse(email_logger.list_of_recipients)
        self.assertIsInstance(email_logger.list_of_recipients, set)

        email_logger.add_new_recipient(TEST_EMAIL)
        email_logger.add_new_recipient(TEST_EMAIL_2)
        
        num_of_recipients_added = len(email_logger.list_of_recipients)
        self.assertCountEqual(email_logger.list_of_recipients, [TEST_EMAIL, TEST_EMAIL_2], 
                              msg=f"Expected the list of recipients to be 2 but got {len(email_logger.list_of_recipients)}")
    