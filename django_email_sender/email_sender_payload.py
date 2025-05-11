from dataclasses import dataclass, asdict
import json
from typing import Any
from dataclasses import asdict

from django_email_sender.utils import sanitize_for_json


class EmailBase:
    def to_json(self):
    
        email_payload_dict = asdict(self)
        cleaned_payload    = sanitize_for_json(email_payload_dict)
        return json.dumps(cleaned_payload, indent=4)



@dataclass
class EmailPayload(EmailBase):
    """
    Represents the full payload of an email before it is sent.

    Attributes:
        from_email (str): The sender's email address.
        to_email (str): The recipient's email address.
        subject (str): The subject of the email.
        body_html (str): The HTML content of the email body.
        body_text (str): The plain text content of the email body.
        context (dict): Context data used for template rendering.
        headers (dict): Custom headers to include with the email.
    """

    from_email: str
    to_email: str
    subject: str
    body_html: str
    body_text: str
    context: dict
    headers: dict

    def is_valid(self):
        """
        Validates whether the payload contains the minimum required fields.

        Returns:
            bool: True if all required fields are present and non-empty, False otherwise.
        """
        return bool(self.from_email and self.to_email and self.subject and self.body_html and self.body_text)


@dataclass(frozen=True)
class EmailMetaData(EmailBase):
    """
    Captures metadata about an email send attempt.

    Attributes:
        to_email (str): The recipient's email address.
        subject (str): The subject of the email.
        status (str): The result status of the send attempt (e.g., "success", "failed").
        timestamp (str): The timestamp of the attempt, typically in ISO format.
        errors (Any): Any error details captured during the send attempt.
    """

    to_email: str
    subject: str
    status: str
    timestamp: str
    errors: Any

    def is_valid(self):
        """
        Validates whether the metadata contains all required fields.

        Returns:
            bool: True if all required fields are present and non-empty, False otherwise.
        """
        return bool(self.to_email and self.subject and self.status and self.timestamp)
