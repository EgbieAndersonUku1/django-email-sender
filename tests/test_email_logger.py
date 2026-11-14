import json
import logging
import uuid
from django.core import mail
from django.test import TestCase
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.email_sender import EmailSender
from django_email_sender.email_sender_constants import LoggerType
from django_email_sender.exceptions import InvalidIdempotencyKey


class TestEmailSenderLogger(TestCase):
    def setUp(self):
        self.py_logger = logging.getLogger("test_email_sender")
        self.logger = (
            EmailSenderLogger.create()
            .start_logging_session()
            .config_logger(self.py_logger, LoggerType.DEBUG)
            .add_email_sender_instance(EmailSender.create())
        )

    def test_with_idempotency_key_accepts_uuid_and_converts_to_str(self):
        key = uuid.uuid4()
        result = self.logger.with_idempotency_key(key)

        self.assertIs(result, self.logger)
        self.assertEqual(self.logger._email_sender.idempotency_key, str(key))

    def test_with_idempotency_key_accepts_string(self):
        self.logger.with_idempotency_key("req-abc-123")
        self.assertEqual(self.logger._email_sender.idempotency_key, "req-abc-123")

    def test_with_idempotency_key_rejects_invalid_type(self):
        with self.assertRaises(InvalidIdempotencyKey) as ctx:
            self.logger.with_idempotency_key(99999)

        self.assertIn("int", str(ctx.exception))

    def test_logger_sends_email_and_records_idempotency_key_in_payload(self):
        key = uuid.uuid4()

        result = (
            self.logger
            .from_address("no-reply@example.com")
            .to("test@example.com")
            .with_subject("Promo Code")
            .with_context({"username": "testuser"})
            .with_text_template("test.txt")
            .with_html_template("test.html")
            .with_idempotency_key(key)
            .send()
        )


        # Verify email was sent with the idempotency header
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.extra_headers["X-Idempotency-Key"], str(key))

        # Verify payload captured the idempotency key
        self.assertEqual(json.loads(self.logger.payload)["idempotency_key"], str(key))
