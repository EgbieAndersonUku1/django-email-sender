import os
from os.path import join
from pathlib import PurePath, Path
from django.test import TestCase


from django_email_sender.email_sender import EmailSender
from django_email_sender.utils import get_template_dirs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dirs                = get_template_dirs()
TEMPLATES_DIR       = dirs["TEMPLATES_DIR"]
EMAIL_TEMPLATES_DIR = dirs["EMAIL_TEMPLATES_DIR"]


class TestEmailSender(TestCase):

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
        
    def test_if_instance_is_created(self):
        self.assertTrue(self.email_sender)
        
    def test_fields(self):
        
        html_path = join(EMAIL_TEMPLATES_DIR, self.html_template)
        text_path = join(EMAIL_TEMPLATES_DIR, self.text_template)
        
        self.assertEqual(self.email_sender.from_email, self.from_email)
        self.assertEqual(self.email_sender.to_email, self.to_email)
        self.assertEqual(self.email_sender.subject, self.subject)
        self.assertEqual(self.email_sender.context, self.context)
        self.assertEqual(self.email_sender.headers, self.headers)
        self.assertEqual(self.email_sender.html_template, html_path)
        self.assertEqual(self.email_sender.text_template, text_path)
    
    def test_clear_from_email_method(self):
        
        self.assertTrue(self.email_sender.from_email)
        self.email_sender.clear_from_email()
        self.assertIsNone(self.email_sender.from_email)
        
    def test_clear_from_email_method(self):
        
        self.assertTrue(self.email_sender.to_email)
        self.email_sender.clear_to_email()
        self.assertFalse(self.email_sender.to_email)
    
    def test_clear_subject_method(self):
        
        self.assertTrue(self.email_sender.subject)
        self.email_sender.clear_subject()
        self.assertIsNone(self.email_sender.subject)
    
    def test_clear_context_method(self):
        
        self.assertTrue(self.email_sender.context)
        self.email_sender.clear_context()
        self.assertFalse(self.email_sender.context)
        self.assertIsInstance(self.email_sender.context, dict)
        
    def test_clear_header_method(self):
        
        self.assertTrue(self.email_sender.headers)
        self.email_sender.clear_headers()
        self.assertFalse(self.email_sender.headers)
        self.assertIsInstance(self.email_sender.headers, dict)
        
    def clear_all_fields(self):
        
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
        
        TEST_EMAIL    = "test@example.com"
        TEST_EMAIL_2  = "test2@example.com"
        
        self.assertFalse(self.email_sender.list_of_recipients)
        self.assertIsInstance(self.email_sender.list_of_recipients, set)

        self.email_sender.add_new_recipient(TEST_EMAIL)
        self.email_sender.add_new_recipient(TEST_EMAIL_2)
        
        num_of_recipients_added = len(self.email_sender.list_of_recipients)
        self.assertCountEqual(self.email_sender.list_of_recipients, [TEST_EMAIL, TEST_EMAIL_2], 
                              msg=f"Expected the list of recipients to be 2 but got {len(self.email_sender.list_of_recipients)}")