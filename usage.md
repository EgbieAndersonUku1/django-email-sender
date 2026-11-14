# `django-email-sender` Usage Guide

> **Version 2.1.0** — Includes optional idempotency-key metadata. The package does **not** deduplicate messages; your application owns that decision.

## Overview

`django-email-sender` provides a chainable interface for sending Django template-based plain-text and HTML emails. You can use `EmailSender` on its own or opt into logging and application-owned database persistence with `EmailSenderLogger`.

## Installation

```bash
pip install django-email-sender

```

Configure a Django email backend before sending messages. For local development, Django's console backend is a useful starting point:

```python
# settings.py — development only

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = "no-reply@example.com"

```

For an SMTP provider, configure the credentials and connection details supplied by that provider:

```python
# settings.py — illustrative SMTP configuration

import os

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ["EMAIL_HOST"]

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]

EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

```

Never commit real SMTP passwords to source control. For Gmail, a provider-approved authentication method (such as an app password, where available) may be required.

## Basic Usage

### 1. Create email templates

For example, create these files in your Django project's template directory:

```text
templates/

└── verification/

    ├── verification.txt

    └── verification.html

```

`templates/verification/verification.txt`:

```django
Hello {{ username }},

Your verification code is {{ verification_code }}.

```

`templates/verification/verification.html`:

```django
\<p>Hello {{ username }},\</p>

\<p>Your verification code is \<strong>{{ verification_code }}\</strong>.\</p>

```

Ensure Django can discover the templates:

```python
# settings.py (inside your existing TEMPLATES configuration)

"DIRS": [BASE_DIR / "templates"],

"APP_DIRS": True,

```

### 2. Send an email

```python
from django_email_sender.email_sender import EmailSender

response_count, is_sent = (

    EmailSender.create()

    .from_address("no-reply@example.com")

    .to("test@example.com")

    .with_subject("Verify Your Email")

    .with_context({"username": "John", "verification_code": "123456"})

    .with_html_template("verification.html", folder_name="verification")

    .with_text_template("verification.txt", folder_name="verification")

    .send()

)

```

`send()` returns `(response_count, is_sent)` in the implementation reviewed for v2.1.0. `is_sent` indicates that the configured Django email backend reported a successful send; it does not guarantee delivery to the recipient's inbox.

### 3. Optional local test view

For a quick **development-only** test, add a view in `core/views.py`:

```python
from django.http import HttpResponse

from django_email_sender.email_sender import EmailSender

def test_email_view(request):

    response_count, is_sent = (

        EmailSender.create()

        .from_address("no-reply@example.com")

        .to("test@example.com")

        .with_subject("Verify Your Email")

        .with_context({"username": "John", "verification_code": "123456"})

        .with_html_template("verification.html", folder_name="verification")

        .with_text_template("verification.txt", folder_name="verification")

        .send()

    )

    return HttpResponse(f"Email backend accepted {response_count} message(s): {is_sent}")

```

In `core/urls.py`:

```python
from django.urls import path

from .views import test_email_view

urlpatterns = [

    path("send-verification-email/", test_email_view),

]

```

Include the app's URLs in your project's URL configuration if they are not already included, then run:

```bash
python manage.py runserver

```

Visit `http\://127.0.0.1:8000/send-verification-email/` to test locally. **Remove or protect this endpoint before deployment**: sending emails from an unrestricted GET request can be abused and can trigger repeated sends.

## Advanced Usage

### Adding multiple recipients

`.to(recipient)` accepts either a single email address (`str`) or a list of addresses (`list[str]`) for backward compatibility. **When passed a list, it uses only the first address**; it does not add every address in the list. An empty list or `None` leaves the current recipient unchanged.

```python
sender = EmailSender.create().to("first@example.com")

# Backward-compatible: uses only "first@example.com"

sender.to(["first@example.com", "ignored@example.com"])

# To send to multiple recipients, add them explicitly:

sender.add_new_recipient("second@example.com")

sender.add_new_recipient("third@example.com")

```

Calling `.to()` again **replaces** the primary recipient; use `.add_new_recipient()` to add recipients rather than replacing it.

### Idempotency keys — new in v2.1.0

`.with_idempotency_key(idempotency_key)` accepts a `str` or `uuid.UUID` and attaches its string representation to the outgoing `X-Idempotency-Key` email header. It is available on both `EmailSender` and `EmailSenderLogger`. The logger's JSON payload also includes the key for audit inspection.

```python
import uuid

from django_email_sender.email_sender import EmailSender

# In a real retry workflow, reuse the key for the SAME logical operation.

operation_key = uuid.uuid4()

response_count, is_sent = (

    EmailSender.create()

    .from_address("no-reply@example.com")

    .to("customer@example.com")

    .with_subject("Payment Receipt")

    .with_context({"amount": "£25.00"})

    .with_html_template("receipt.html", folder_name="billing")

    .with_text_template("receipt.txt", folder_name="billing")

    .with_idempotency_key(operation_key)

    .send()

)

```

**Important:** This header is **metadata, not automatic duplicate prevention**. Calling `.send()` twice with the same key can send two emails. DjangoEmailSender does not store keys, check for previous sends, or coordinate concurrent workers. Generate a stable key once per logical operation and reuse it for retries; generating a fresh UUID on each retry defeats application-level duplicate detection.

#### Application-owned `EmailOutbox` pattern (optional)

If your application needs deduplication, it can own an `EmailOutbox` table with a **unique idempotency key**, message status, timestamps, and retry information. The application can reserve a key before sending, decide whether to retry, and record the outcome. Coordinate concurrent workers with database transactions or another appropriate locking mechanism.

A unique database key alone is not an exactly-once delivery guarantee: the email backend may accept a message before your application can record success. Your application should explicitly decide how to handle uncertain outcomes. **No `EmailOutbox` model is supplied or required by this library.**

### Customising the logger

Use `EmailSenderLogger` when you want logging in addition to sending. Logging is opt-in.

```python
import logging

import uuid

from django_email_sender.email_sender import EmailSender

from django_email_sender.email_logger import EmailSenderLogger

from django_email_sender.email_sender_constants import LoggerType

email_logger = (

    EmailSenderLogger.create()

    .start_logging_session()

    .config_logger(logging.getLogger("email_sender"), LoggerType.DEBUG)

    .add_email_sender_instance(EmailSender.create())

)

# The logger wrapper also supports:

email_logger.with_idempotency_key(uuid.uuid4())

```

The `LoggerType` import follows the path used in the project README; verify it against your installed package before running the example.

For application-specific error formatting, supply a formatter that accepts an exception and optionally a traceback string, following the logger's documented configuration API:

```python
def custom_email_formatter(exc: Exception, trace: str | None = None) -> str:

    detail = str(exc)

    return f"Email error: {type(exc).__name__}: {detail}; traceback: {trace or 'unavailable'}"

```

Configure Python's `logging` handlers in your application rather than assuming the email sender's internal logger is publicly accessible:

```python
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("email_sender")

```

## Database Configuration (optional)

`EmailSenderLogger` can persist email metadata when you provide your own model and explicitly enable saving. It does not create your application's database table for you.

### Define your log model

```python
# your_app/models.py

from django.db import models

from django_email_sender.models import EmailBaseLog

class CustomEmailLog(EmailBaseLog):

    request_id = models.CharField(max_length=100, null=True, blank=True)

    environment = models.CharField(max_length=20, default="production")

```

`EmailBaseLog` is an abstract model; Django creates a table for your concrete subclass, not for the abstract base. Then run:

```bash
python manage.py makemigrations

python manage.py migrate

```

### Enable metadata persistence

```python
from django_email_sender.email_sender import EmailSender

from django_email_sender.email_logger import EmailSenderLogger

from your_app.models import CustomEmailLog

email_logger = (

    EmailSenderLogger.create()

    .start_logging_session()

    .add_email_sender_instance(EmailSender.create())

    .add_log_model(CustomEmailLog)

    .enable_email_meta_data_save()

)

# Configure the message (including both templates) before calling email_logger.send().

```

Database persistence is opt-in. Adding a model does not by itself enable saving. Your application is responsible for migrations and for any separate `EmailOutbox` or deduplication workflow.

## Clearing Fields

Use field-specific clearing methods to reset parts of a configured sender:

```python
sender.clear_subject()

sender.clear_to_email()

sender.clear_html_template()

sender.clear_text_template()

```

To reset all configured fields, call:

```python
sender.clear_all_fields()

```

You can also use `.send(auto_reset=True)` to clear the sender fields after sending. In v2.1.0, `clear_all_fields()` resets the sender state, including the idempotency key. If you intend to retry the same logical operation after a reset, retain the key in your consuming application and explicitly attach it again using `.with_idempotency_key(key)`. The v2.1.0 release also fixes enum-backed field-name handling during clearing.

## Running Tests

If you have cloned the **source repository**, run its test suite from the repository root:

```bash
python runtests.py

```

The v2.1.0 tests reviewed cover accepting string/UUID idempotency keys, rejecting invalid types, attaching the outgoing header, and including the key in logger payloads. Additional useful regression tests are repeated sends with the same key (confirming no built-in deduplication) and verifying that `auto_reset=True` clears the idempotency key. These are suggested tests, not claims that they have already been added or run.

## Version History and License

See [VERSION_HISTORY.md](VERSION_HISTORY.md) for release notes and migration guidance, and [LICENCE](LICENCE) for the MIT license.
