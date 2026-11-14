import uuid
from unittest.mock import patch
from django.core import mail
from django.test import TestCase
from django_email_sender.email_sender import EmailSender
from django_email_sender.exceptions import (
    EmailSendError,
    EmailTemplateNotFound,
    IncorrectEmailSenderFieldType,
    InvalidIdempotencyKey,
)


class TestEmailSender(TestCase):
    def setUp(self):
        """Create a valid, reusable EmailSender builder for each test."""
        self.idempotency_key = uuid.uuid4()
        self.sender = (
            EmailSender.create()
            .from_address("no-reply@example.com")
            .to(["test@example.com"])
            .with_subject("Test Email")
            .with_context({"username": "testuser"})
            .with_text_template("test.txt")
            .with_html_template("test.html")
            .with_idempotency_key(self.idempotency_key)
        )

    def test_email_sender_creates_and_sends_email(self):
        """Test end-to-end email creation, template rendering, headers, and sending."""
        self.assertEqual(self.sender.from_email, "no-reply@example.com")
        self.assertEqual(self.sender.subject, "Test Email")
        self.assertEqual(self.sender.idempotency_key, str(self.idempotency_key))

        resp, is_sent = self.sender.send()

        self.assertEqual(resp, 1)
        self.assertTrue(is_sent)
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.from_email, "no-reply@example.com")
        self.assertEqual(sent_email.to, ["test@example.com"])
        self.assertEqual(sent_email.subject, "Test Email")
        self.assertEqual(sent_email.body.strip(), "Hello testuser")
        self.assertEqual(
            sent_email.extra_headers["X-Idempotency-Key"],
            str(self.idempotency_key),
        )
        self.assertEqual(sent_email.alternatives[0][0].strip(), "<p>Hello testuser</p>")

    def test_send_without_idempotency_key_omits_header(self):
        """Test sending an email when no idempotency key is provided."""
        sender = (
            EmailSender.create()
            .from_address("no-reply@example.com")
            .to(["user@example.com"])
            .with_subject("No Key Email")
            .with_context({"username": "alice"})
            .with_text_template("test.txt")
            .with_html_template("test.html")
        )

        resp, is_sent = sender.send()

        self.assertEqual(resp, 1)
        self.assertTrue(is_sent)
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn("X-Idempotency-Key", mail.outbox[0].extra_headers)

    def test_idempotency_key_accepts_string_and_rejects_invalid_types(self):
        """Test that string keys are accepted and invalid types raise InvalidIdempotencyKey."""
        self.sender.with_idempotency_key("custom-key-123")
        self.assertEqual(self.sender.idempotency_key, "custom-key-123")

        with self.assertRaises(InvalidIdempotencyKey):
            self.sender.with_idempotency_key(12345)

    def test_auto_reset_clears_fields_after_sending(self):
        """Test that auto_reset=True resets builder attributes after a successful send."""
        resp, is_sent = self.sender.send(auto_reset=True)

        self.assertEqual(resp, 1)
        self.assertTrue(is_sent)
        self.assertIsNone(self.sender.from_email)
        self.assertIsNone(self.sender.subject)
        self.assertIsNone(self.sender.text_template)
        self.assertIsNone(self.sender.html_template)

    def test_missing_required_fields_raises_validation_error(self):
        """Test that sending an incomplete email raises an exception."""
        incomplete_sender = EmailSender.create().from_address("no-reply@example.com")

        with self.assertRaises(Exception):
            incomplete_sender.send()

    def test_missing_template_file_raises_email_template_not_found(self):
        """Test that specifying a non-existent template raises EmailTemplateNotFound."""
        self.sender.with_text_template("does_not_exist.txt")

        with self.assertRaises(EmailTemplateNotFound):
            self.sender.send()

    def test_send_failure_raises_email_send_error(self):
        """Test that an EmailSendError during delivery is properly caught and re-raised."""
        with patch(
            "django_email_sender.email_sender.EmailMultiAlternatives.send",
            side_effect=EmailSendError(message="SMTP connection refused"),
        ):
            with self.assertRaises(EmailSendError):
                self.sender.send()

    def test_same_idempotency_key_does_not_prevent_repeated_sends(self):
        """
        Verify that idempotency keys are metadata, not
        an automatic duplicate-prevention mechanism.

        Deduplication is the consuming application's responsibility.
        """
        first_response, first_sent = self.sender.send()
        second_response, second_sent = self.sender.send()

        self.assertEqual(first_response, 1)
        self.assertEqual(second_response, 1)
        self.assertTrue(first_sent)
        self.assertTrue(second_sent)

        self.assertEqual(len(mail.outbox), 2)

        for email in mail.outbox:
            self.assertEqual(
                email.extra_headers["X-Idempotency-Key"],
                str(self.idempotency_key),
            )

    def test_to_accepts_string_and_list_for_backward_compatibility(self):
        """Test that to() accepts strings and lists but sets one primary recipient."""

        # A single string sets the recipient.
        self.sender.to("first@example.com")
        self.assertEqual(self.sender.to_email, "first@example.com")

        # A list containing one address is supported.
        self.sender.to(["second@example.com"])
        self.assertEqual(self.sender.to_email, "second@example.com")

        # A list containing multiple addresses uses only the first.
        self.sender.to([
            "third@example.com",
            "fourth@example.com",
        ])
        self.assertEqual(self.sender.to_email, "third@example.com")

        # An empty list does not overwrite the existing recipient.
        self.sender.to([])
        self.assertEqual(self.sender.to_email, "third@example.com")

        # None does not overwrite the existing recipient.
        self.sender.to(None)
        self.assertEqual(self.sender.to_email, "third@example.com")

        # Calling to() again replaces the primary recipient.
        self.sender.to("fifth@example.com")
        self.assertEqual(self.sender.to_email, "fifth@example.com")

    def test_to_returns_sender_instance_for_chaining(self):
        """Test that to() returns the current EmailSender instance."""

        result = self.sender.to("first@example.com")

        self.assertIs(result, self.sender)

    def test_add_new_recipient_adds_multiple_recipients(self):
        """
        Verify that add_new_recipient() preserves the primary
        recipient, adds additional recipients without duplicates,
        and supports method chaining.

        Additional recipients may appear in any order because
        they are stored in a set.
        """
        result = (
            self.sender
            .add_new_recipient("second@example.com")
            .add_new_recipient("third@example.com")
        )

        # Verify method chaining.
        self.assertIs(result, self.sender)

        # Send the email and verify the response.
        resp, is_sent = self.sender.send()

        self.assertEqual(resp, 1)
        self.assertTrue(is_sent)
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]

        # Verify that the primary recipient remains first.
        self.assertEqual(
            sent_email.to[0],
            "test@example.com",
        )

        # Verify additional recipients regardless of order.
        self.assertCountEqual(
            sent_email.to[1:],
            [
                "second@example.com",
                "third@example.com",
            ],
        )

        # Verify that no duplicate recipients were added.
        self.assertEqual(len(sent_email.to), 3)

    def test_add_new_recipient_adds_unique_recipients(self):
        """
        Verify that add_new_recipient() adds unique recipients,
        prevents duplicates, and supports method chaining.
        """
        result = (
            self.sender
            .add_new_recipient("second@example.com")
            .add_new_recipient("third@example.com")
            .add_new_recipient("second@example.com")
        )

        # Verify method chaining.
        self.assertIs(result, self.sender)

        # Verify duplicates are not stored.
        self.assertEqual(
            self.sender.list_of_recipients,
            {
                "second@example.com",
                "third@example.com",
            },
        )

        # Verify recipients are included in the outgoing email.
        resp, is_sent = self.sender.send()

        self.assertEqual(resp, 1)
        self.assertTrue(is_sent)
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]

        # Sets do not guarantee recipient ordering.
        self.assertCountEqual(
            sent_email.to,
            [
                "test@example.com",
                "second@example.com",
                "third@example.com",
            ],
        )

    def test_add_new_recipient_ignores_empty_values_and_rejects_invalid_types(self):
        """Verify that empty values are ignored and invalid types are rejected."""

        # Empty values should not change the recipient set.
        self.assertIs(self.sender.add_new_recipient(""), self.sender)
        self.assertIs(self.sender.add_new_recipient(None), self.sender)
        self.assertEqual(len(self.sender.list_of_recipients), 0)

        # Invalid non-empty types should raise an exception.
        with self.assertRaises(IncorrectEmailSenderFieldType):
            self.sender.add_new_recipient(123)

    def test_primary_recipient_is_not_duplicated(self):
        """Ensure the primary recipient appears only once in the sent email."""

        self.sender.add_new_recipient("test@example.com")
        self.sender.add_new_recipient("second@example.com")

        self.sender.send()

        recipients = mail.outbox[0].to

        self.assertEqual(
            recipients.count("test@example.com"),
            1,
        )
        self.assertIn("second@example.com", recipients)


    def test_idempotency_key_persists_without_auto_reset(self):
        """Ensure the key remains attached when auto_reset is disabled."""

        self.sender.send(auto_reset=False)

        self.assertEqual(
            self.sender.idempotency_key,
            str(self.idempotency_key),
        )

        self.assertEqual(
            mail.outbox[0].extra_headers["X-Idempotency-Key"],
            str(self.idempotency_key),
    )

    def test_empty_idempotency_key_omits_header(self):
        """An empty string is accepted but does not create a header."""

        self.sender.with_idempotency_key("")

        self.sender.send()

        self.assertNotIn(
            "X-Idempotency-Key",
            mail.outbox[0].extra_headers,
        )
