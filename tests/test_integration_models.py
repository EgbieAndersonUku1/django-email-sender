from django.test import TestCase

from django_email_sender.email_sender import EmailSender
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.exceptions import TemplateDirNotFound, IncorrectEmailSenderInstance
from django_email_sender.email_sender_constants import EmailSenderConstants as EmailSenderFieldConstants
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
        self.email_sender_logger    = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
        self.EXPECTED_NUM_OF_FIELDS = 9
        self.email_fields           = self._get_email_field_value_list()
    
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
    
    
    def test_fields_can_be_added_to_exclusion_list(self):
        """
        Test that fields can be added to the exclusion list, and the proper flags
        set, so that when added in the views it consequently excluded from logging.

        This verifies that:
        - Fields added to the exclusion list appear in the internal exclusion set.
        - Being in the exclusion list means those fields will not be logged.
        - Relevant flags are updated to reflect that exclusion-based logging is enabled.
        - Inclusive logging remains disabled, ensuring excluded fields are not logged.

        This reflects the behavior expected when fields are added via UI or constants.
        """
        
        email_logger_instance = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
        self.assertTrue(email_logger_instance)     

        # Initially, both inclusive and exclusion trace logging flags should be disabled
        self.assertFalse(email_logger_instance._enable_field_trace_logging)
        self.assertFalse(email_logger_instance._enable_exclusion_field_trace)
        
        # Exclusion list should be empty at the start
        self.assertEqual(len(email_logger_instance._exclude_fields), 0)
        
        email_logger_instance.exclude_fields_from_logging(*self.email_fields)

        # Assert that the fields to exclude have been added correctly to the exclusion set
        self._assert_email_fields_in_set(email_logger_instance._exclude_fields)
    
        # Verify the number of excluded fields matches expectation
        self.assertEqual(
            len(email_logger_instance._exclude_fields), 
            self.EXPECTED_NUM_OF_FIELDS, 
            msg=f"Fields: {email_logger_instance._exclude_fields}"
        ) 
        
        # Confirm exclusion-based trace logging is enabled,
        # while inclusive trace logging remains disabled to prevent logging of excluded fields
        self.assertFalse(email_logger_instance._enable_field_trace_logging)
        self.assertTrue(email_logger_instance._enable_exclusion_field_trace)
        
        # Inclusive logging fields list should be empty, indicating no fields are included in inclusive logging
        self.assertFalse(email_logger_instance._fields)

    def test_fields_can_be_added_to_inclusion_list(self):
        """
        Test that fields can be added to the inclusion list and the proper flags
        set, so that when it is called in the view, only those fields are logged.

        This verifies that:
            - Fields added to the inclusion list appear in the internal inclusion set.
            - Only fields in the inclusion list are logged.
            - Relevant flags are updated to reflect that inclusive logging is enabled.
            - Exclusion-based logging remains disabled to prevent conflicting behavior.

        This reflects the behavior expected when fields are specified via UI or constants
        to restrict logging exclusively to those fields.
        """
        
        email_logger_instance = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
        self.assertTrue(email_logger_instance)         

        # Initially, both inclusive and exclusion trace logging flags should be disabled
        self.assertFalse(email_logger_instance._enable_field_trace_logging)
        self.assertFalse(email_logger_instance._enable_exclusion_field_trace)
            
        # Inclusion list should be empty at the start
        self.assertEqual(len(email_logger_instance._fields), 0)
            
        email_logger_instance.log_only_fields(*self.email_fields)
            
        # Verify the number of included fields matches expectation
        self.assertEqual(
            len(email_logger_instance._fields), 
            self.EXPECTED_NUM_OF_FIELDS, 
            msg=f"Fields: {email_logger_instance._fields}"
           ) 
            
        # Confirm inclusive trace logging is enabled,
        # while exclusion-based trace logging remains disabled
        self.assertTrue(email_logger_instance._enable_field_trace_logging)
        self.assertFalse(email_logger_instance._enable_exclusion_field_trace)
            
        # Exclusion list should be empty, indicating no fields are excluded
        self.assertFalse(email_logger_instance._exclude_fields)

        
    def _assert_email_fields_in_set(self, field_set_name: str):
        """
        Assert that all defined email fields (excluding EMAIL_ID) exist in the provided field set.

        This helper method checks that each field's value, except EMAIL_ID, is present
        in the given set. It is used to confirm that expected fields have been added
        to an inclusion or exclusion list.

        Args:
            field_set_name (set): The set of field names to check against.
        """
        for email_field in EmailSenderFieldConstants.Fields:
            if email_field.value == EmailSenderFieldConstants.Fields.EMAIL_ID:
                continue
            self.assertIn(email_field.value, field_set_name, msg=f"Field {email_field} is not found")

    
    def _get_email_field_value_list(self):
        """
        Return a list of string values for all email fields defined in EmailSenderFieldConstants.Fields,
        excluding EMAIL_ID.

        This helper is typically used to generate test inputs for inclusion or exclusion lists.

        Returns:
            list: A list of field values (strings).
        """
        return [field.value for field in EmailSenderFieldConstants.Fields]
    
    def test_start_logging_session_flags_are_set_when_method_is_called(self):
        """
        Test that when the `start_logging_session` is called the appropriate
        flags are set.
        """
        
        email_logger_instance = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
        self.assertFalse(email_logger_instance._logging_enabled)
        self.assertFalse(email_logger_instance._logger_started)
        
        # start the logging session
        resp = email_logger_instance.start_logging_session()
        
        # check the flags
        self.assertTrue(email_logger_instance._logging_enabled)
        self.assertTrue(email_logger_instance._logger_started)
        
        # check that it returns an instance of EmailSenderLogger
        self.assertIsInstance(resp, EmailSenderLogger)
    
    def test_stop_logging_session_flags_are_set_when_method_is_called(self):
        """
        Test that when the `stop_logging_session` is called the appropriate
        flags are set.
        """
        
        # start the start_logging session and check the flag
        email_logger_instance = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
        email_logger_instance.start_logging_session()
        
        # check the flags are turned on
        self.assertTrue(email_logger_instance._logging_enabled)
        self.assertTrue(email_logger_instance._logger_started)
        
        # stop the logging session and check the flags
        resp = email_logger_instance.stop_logging_session()
        
        # check the flags are turned off
        self.assertFalse(email_logger_instance._logging_enabled)
        self.assertFalse(email_logger_instance._logger_started)
        
        # check that it returns an instance of EmailSenderLogger
        self.assertIsInstance(resp, EmailSenderLogger)
        
    def test_pause_logging_session_flags_are_set_when_method_is_called(self):
        """
        Test that when the `pause_logging_session` is called the appropriate
        flags are set.
        """
        email_logger_instance = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
        email_logger_instance.start_logging_session()
        
        # test the neccessary flags are turned on when start session method is called
        self.assertTrue(email_logger_instance._logging_enabled)
        self.assertTrue(email_logger_instance._logger_started)

        # call the pause logging
        resp = email_logger_instance.pause_logging()
        
        # test the `enabled flag`` is now False but `logger_started` is still `True`
        self.assertFalse(email_logger_instance._logging_enabled)
        self.assertTrue(email_logger_instance._logger_started)
        
        # check that it returns an instance of EmailSenderLogger
        self.assertIsInstance(resp, EmailSenderLogger)
        
    def test_resume_logging_session_flags_are_set_when_method_is_called(self):
        """
        Test that when the `resume_logging_session` is called the appropriate
        flags are set.
        
        """
        email_logger_instance = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
        email_logger_instance.start_logging_session()
        
        # test the neccessary flags are turned on when start session method is called
        self.assertTrue(email_logger_instance._logging_enabled)
        self.assertTrue(email_logger_instance._logger_started)
        
        # call the resume logging
        resp = email_logger_instance.pause_logging()
        
        # test the `enabled flag`` is now False but `logger_started` is still `True`
        self.assertFalse(email_logger_instance._logging_enabled)
        self.assertTrue(email_logger_instance._logger_started)
        
        # check that it returns an instance of EmailSenderLogger
        self.assertIsInstance(resp, EmailSenderLogger) 
    
    def test_enable_verbose_flag_is_set_after_call(self):
        """
        Test that when the `enable_verbose_flag` is called the appropriate
        flags are set.
        
        """
        # check if enable verbose is set to false to before call
        self.assertFalse(self.email_sender_logger._debug_verbose)
        
        # call the enable verbose method and the check if it s now True
        resp = self.email_sender_logger.enable_verbose()
        self.assertTrue(self.email_sender_logger._debug_verbose)
        
        # check that it returns an instance of EmailSenderLogger
        self.assertIsInstance(resp, EmailSenderLogger) 
        
    def test_disable_verbose_flag_is_set_after_call(self):
        """
        Test that calling `disable_verbose` clears the `_debug_verbose` flag.

        Verifies that `_debug_verbose` is initially False, set to True after calling 
        `enable_verbose`, and then reset to False after calling `disable_verbose`.
        """
        # check if enable verbose is set to false to before call
        self.assertFalse(self.email_sender_logger._debug_verbose)
        
        # call the enable verbose method and check if it now True
        self.email_sender_logger.enable_verbose()
        self.assertTrue(self.email_sender_logger._debug_verbose)
        
        # disable verbose and check if the flag is now False
        resp = self.email_sender_logger.disable_verbose()
        self.assertFalse(self.email_sender_logger._debug_verbose)
        
        # check that it returns an instance of EmailSenderLogger
        self.assertIsInstance(resp, EmailSenderLogger) 
                
    def tearDown(self):
        self.email_sender_logger = create_email_logger_instance(EmailSenderConstants, EmailSender.create())
        

    
    
    