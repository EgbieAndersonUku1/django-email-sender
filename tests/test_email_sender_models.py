import os
from os.path import join
from pathlib import PurePath, Path
from django.test import TestCase
from unittest.mock import Mock, patch

from django_email_sender.email_sender import EmailSender
from django_email_sender.utils import get_template_dirs
from django_email_sender.exceptions import TemplateDirNotFound
from .test_fixture import (EmailSenderConstants, 
                           create_email_sender_instance,
                           create_template_path,
                           test_missing_template,
                           TEMPLATES_DIR,
                           EMAIL_TEMPLATES_DIR,
                           create_email_logger_instance
                           )

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class TestEmailSender(TestCase):

    def setUp(self):  
        self.email_sender  = create_email_sender_instance(EmailSenderConstants)
              
    def test_if_instance_is_created(self):
        self.assertTrue(self.email_sender)
    
    def test_error_is_raised_when_email_template_folder_is_missing(self):
        """"""
        EXCEPTION_ERROR = "[TemplateDirNotFound] Primary template [Templates] is missing,  category=TEMPLATE, action=MISSING_PRIMARY"
        email_sender    = create_email_sender_instance(EmailSenderConstants)
              
        with self.assertRaises(TemplateDirNotFound) as custom_message:
            email_sender.send()
        
        exc = custom_message.exception
        self.assertIsInstance(exc, TemplateDirNotFound)
        self.assertEqual(str(exc), EXCEPTION_ERROR)
    
    def test_error_if_raised_when_template_folder_is_missing(self):
       """
        Ensure that a TemplateDirNotFound error is raised when the template 
        directory is missing.

        This test avoids creating actual template paths during testing. Since the 
        templates directory does not exist, attempting to send an email using 
        EmailSender should raise a TemplateDirNotFound error with the expected 
        message.
       """
        
       MISSING_TEMPLATE_PATH =  TEMPLATES_DIR
       EXCEPTION_ERROR       = "[TemplateDirNotFound] Primary template [Templates] is missing,  category=TEMPLATE, action=MISSING_PRIMARY"

       email_sender   = create_email_sender_instance(EmailSenderConstants)
       html_template  = create_template_path(EmailSenderConstants.text_template, email_templates_dir=TEMPLATES_DIR)
       text_template  = create_template_path(EmailSenderConstants.html_template, email_templates_dir=TEMPLATES_DIR )
            
       EmailSenderConstants.html_template = html_template
       EmailSenderConstants.text_template  = text_template
        
       with self.assertRaises(TemplateDirNotFound) as custom_message:
           email_sender.send()

       exc = custom_message.exception
       self.assertIsInstance(exc, TemplateDirNotFound)
       self.assertEqual(str(exc), EXCEPTION_ERROR)
    
    def test_fields(self):
        """
        Verifies that all fields on the EmailSender instance are correctly set 
        based on the values provided during initialisation.
        """
        html_path = create_template_path(EmailSenderConstants.html_template)
        text_path = create_template_path(EmailSenderConstants.text_template)
        
        self.assertEqual(self.email_sender.from_email, EmailSenderConstants.from_email)
        self.assertEqual(self.email_sender.to_email, EmailSenderConstants.to_email)
        self.assertEqual(self.email_sender.subject,  EmailSenderConstants.subject)
        self.assertEqual(self.email_sender.context,  EmailSenderConstants.context)
        self.assertEqual(self.email_sender.headers,  EmailSenderConstants.headers)
        self.assertEqual(self.email_sender.html_template, html_path)
        self.assertEqual(self.email_sender.text_template, text_path)
    
    def test_to_email_accepts_list(self):
        """
        Ensures that the 'to_email' field can accept an email 
        when passed to the EmailSender instance as a list.
        """
        EmailSenderConstants.to_email = ["test@example.com"]

        self.assertIsInstance(EmailSenderConstants.to_email, list)

        email_sender = create_email_sender_instance(EmailSenderConstants)
        self.assertTrue(email_sender)

    def test_to_email_accepts_string(self):
        """
        Ensures that the 'to_email' field can accept an email address 
        when passed to the EmailSender instance as a string.
        """

        self.assertIsInstance(EmailSenderConstants.to_email, str)
        email_sender = create_email_sender_instance(EmailSenderConstants)
        self.assertTrue(email_sender)
      
    def test_clear_from_email_method(self):
        """
        Verifies that when the ".clear_from_email()" method is called on the "EmailSender"
        class instance then the "from_email" field is cleared.
        """
        self.assertTrue(self.email_sender.from_email)
        self.email_sender.clear_from_email()
        self.assertIsNone(self.email_sender.from_email)
        
    def test_clear_from_email_method(self):
        """
        Verifies that when the ".clear_to_email()" method is called on the "EmailSender"
        class instance then the "to_email" field is cleared.
        """
        self.assertTrue(self.email_sender.to_email)
        self.email_sender.clear_to_email()
        self.assertFalse(self.email_sender.to_email)
    
    def test_clear_subject_method(self):
        """
        Verifies that when the ".clear_subject()" method is called on the "EmailSender"
        class instance then the "subject" field is cleared.
        """
        self.assertTrue(self.email_sender.subject)
        self.email_sender.clear_subject()
        self.assertIsNone(self.email_sender.subject)
    
    def test_clear_context_method(self):
        """
        Verifies that when the ".clear_context()" method is called on the "EmailSender"
        class instance then the "context" field is cleared.
        """
        self.assertTrue(self.email_sender.context)
        self.email_sender.clear_context()
        self.assertFalse(self.email_sender.context)
        self.assertIsInstance(self.email_sender.context, dict)
        
    def test_clear_header_method(self):
        """
        Verifies that when the ".clear_headers()" method is called on the "EmailSender"
        class instance then the "headers" field is cleared.
        """
        self.assertTrue(self.email_sender.headers)
        self.email_sender.clear_headers()
        self.assertFalse(self.email_sender.headers)
        self.assertIsInstance(self.email_sender.headers, dict)
        
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
        self.assertEqual(email_sender.from_email, self.from_email)
        self.assertEqual(email_sender.to_email, self.to_email)
        self.assertEqual(email_sender.subject, self.subject)
        self.assertEqual(email_sender.context, self.context)
        self.assertEqual(email_sender.headers, self.headers)
        
        self.assertEqual(email_sender.html_template, html_path)
        self.assertEqual(email_sender.text_template, text_path)
        
        
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
        Ensures that when the `.add_new_recipient()` method is called
        a new recipient email is added to the list of recipients to 
        send an email to.
        """
        TEST_EMAIL    = "test@example.com"
        TEST_EMAIL_2  = "test2@example.com"
        
        self.assertFalse(self.email_sender.list_of_recipients)
        self.assertIsInstance(self.email_sender.list_of_recipients, set)

        self.email_sender.add_new_recipient(TEST_EMAIL)
        self.email_sender.add_new_recipient(TEST_EMAIL_2)
        
        num_of_recipients_added = len(self.email_sender.list_of_recipients)
        self.assertCountEqual(self.email_sender.list_of_recipients, [TEST_EMAIL, TEST_EMAIL_2], 
                              msg=f"Expected the list of recipients to be 2 but got {len(self.email_sender.list_of_recipients)}")
    
    
    def tearDown(self):
        # Reset any modified fields since one of the fields is set to a list for
        EmailSenderConstants.to_email = "to-reply@example.com"
        EmailSenderConstants.from_email = "no-reply@example.com"