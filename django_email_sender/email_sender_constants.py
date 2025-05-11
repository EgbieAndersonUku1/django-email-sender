from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from django.utils.translation import gettext_lazy as _


class EmailSenderConstants:
    """
    Container class for constants used in the email sending system.
    Contains nested Enums for field keys and public method names.
    """

    class Fields(Enum):
        """Enum representing the internal keys used for sending emails."""
        FROM_EMAIL        = "from_email"
        TO_EMAIL          = "to_email"
        SUBJECT           = "subject"
        HTML_TEMPLATE     = "html_template"
        TEXT_TEMPLATE     = "text_template"
        CONTEXT           = "context"
        HEADERS           = "headers"
        LIST_OF_RECIPIENT = "list_of_recipients"
        EMAIL_ID          = "email_id"

        @classmethod
        def is_valid_field(cls, field_name: str) -> bool:
            """
            Check if the given field name is a valid field in the enum.
            
            Args:
                field_name (str): The name of the field to validate.
            
            Returns:
                bool: True if valid, False otherwise.
            """
            return field_name in {f.value for f in cls}

    class PublicMethods(Enum):
        """Enum representing the public method names available for chaining."""
        FROM_EMAIL    = "from_address"
        TO_EMAIL      = "to"
        SUBJECT       = "with_subject"
        HTML_TEMPLATE = "with_html_template"
        TEXT_TEMPLATE = "with_text_template"
        HEADERS       = "with_headers"
        CONTEXT       = "with_context"
        SEND          = "send"
        CREATE        = "create"
        ADD_RECIPIENT = "add_new_recipient"


@dataclass(frozen=True)
class LoggerType:
    """Constants representing different logger levels."""
    INFO: str    = "info"
    WARNING: str = "warning"
    ERROR: str   = "error"
    DEBUG: str   = "debug"



def get_email_sender_param_contract():
    return {
        'FROM_EMAIL': {
            'method': 'from_address',
            'params': {'email': str},
        },
        'TO_EMAIL': {
            'method': 'to',
            'params': {'recipient': str},
        },
        'SUBJECT': {
            'method': 'with_subject',
            'params': {'subject': str},
        },
        'HTML_TEMPLATE': {
            'method': 'with_html_template',
            'params': {'template_name': str, 'folder_name': str},
        },
        'TEXT_TEMPLATE': {
            'method': 'with_text_template',
            'params': {'template_name': str, 'folder_name': str},
        },
        'CONTEXT': {
            'method': 'with_context',
            'params': {'context': dict},
        },
        'HEADERS': {
            'method': 'with_headers',
            'params': {'headers': dict },
        },
        'SEND': {
            'method': 'send',
            'params': {},
        },
        'CREATE': {
            'method': 'create',
            'params': {},
        },
        'ADD_RECIPIENT': {
             'method' : 'add_new_recipient',
             'params' : {'recipient': str}
        }
        
        
    }
