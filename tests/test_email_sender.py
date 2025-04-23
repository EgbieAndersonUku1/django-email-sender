from django.test import TestCase
from email_sender.email_sender import EmailSender


class TestEmailSender(TestCase):
    def test_email_sender_creates_and_sends_email(self):
        
        # Example test for email sending logic
        email_sender = EmailSender.create()\
            .from_address("no-reply@example.com")\
            .to(["test@example.com"])\
            .with_subject("Test Email")\
            .with_context({"username": "testuser"})\
            .with_text_template("emails/test.txt")\
            .with_html_template("emails/test.html")
        
        # Test if the sender was set correctly
        self.assertEqual(email_sender.from_address, "no-reply@example.com")
        self.assertEqual(email_sender.subject, "Test Email")

        # Here, you can mock `send_mail` to ensure it gets called
        with self.assertRaises("SomeMockException"):
            email_sender.send()
