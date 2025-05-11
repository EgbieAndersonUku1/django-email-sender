# `django-email-sender` Usage Guide

## Overview

The `django-email-sender` package is a versatile email-sending tool designed to simplify email handling in Django applications. It offers a variety of features, including the ability to send emails using custom templates, handle multiple recipients, integrate with a logger, and persist logs to a database.

This guide will walk you through how to configure and use the package, including advanced features like custom loggers, database integration, and custom email formatting.

---

## Installation

1. **Install the package** via pip:

   ```bash
   pip install django-email-sender
   ```

## Basic Usage


3. **Set up your email backend in `settings.py`** (use the appropriate backend for your email provider):

#### Email settings
```
EMAIL_BACKEND        = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST           = 'smtp.example.com'  # Replace with your email provider's SMTP server
EMAIL_PORT           = 587  # Typically 587 for TLS
EMAIL_USE_TLS        = True  # Enable TLS encryption
EMAIL_HOST_USER      = 'your-email@example.com'  # Your email address
EMAIL_HOST_PASSWORD  = 'your-email-password'  # Your email password (or app password if using 2FA)
DEFAULT_FROM_EMAIL   = EMAIL_HOST_USER  # Default email to send from

```

#### Email settings
```
EMAIL_BACKEND        = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST           = 'smtp.example.com'  # Replace with your email provider's SMTP server
EMAIL_PORT           = 587  # Typically 587 for TLS
EMAIL_USE_TLS        = True  # Enable TLS encryption
EMAIL_HOST_USER      = 'your-email@example.com'  # Your email address
EMAIL_HOST_PASSWORD  = 'your-email-password'  # Your email password (or app password if using 2FA)
DEFAULT_FROM_EMAIL   = EMAIL_HOST_USER  # Default email to send from

```

Note replace
  ``` 
    - smtp.example.com with your-email@example.com
    - your-email-password with your actual email service provider's SMTP details

  ```

If you are using gmail to send emails then the setup would look like 

```
    # Email Backend
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    # Email Settings for Gmail

    EMAIL_USE_TLS        = True  
    EMAIL_HOST           = 'smtp.gmail.com'  
    EMAIL_PORT           = 587  
    EMAIL_HOST_USER      = 'your-email@gmail.com'  # Your Gmail address
    EMAIL_HOST_PASSWORD  = 'your-app-password'     # Use the generated app password (if 2FA is enabled)
    DEFAULT_FROM_EMAIL   = EMAIL_HOST_USER         # Optional: Set default sender email (same as the one above)


```
### Important Notes:

 - App Password: If you have two-factor authentication (2FA) enabled for your Gmail account, you'll need to create an App Password instead of using your   regular Gmail password. You can generate it in your Google account settings.

 - TLS: Setting EMAIL_USE_TLS = True ensures that emails are sent securely over TLS encryption.

This configuration should allow you to send emails via Gmail's SMTP server.


### 🧱 Step 4: Create Email Templates

Create the folder structure :

- See [HTML Email Template Example](#html-email-template-example) and [Plain Text & Multi-part Email Support](#plain-text--multi-part-email-support)
for how to create the files
- Replace the folder `emails` with `verification`
- Do the same with the file names


Then add the templates path in `config/settings.py`:

```python

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # This is where you add the line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

---

### 🧪 Step 5: Add a Test View

In `core/views.py`:

```python
from django.http import HttpResponse
from django_email_sender.email_sender import EmailSender

def test_email_view(request):
    (
    EmailSender.create()
        .from_address("no-reply@example.com")
        .to(["test@example.com"])
        .with_subject("Verify Your Email")
        .with_context({ "username": "John", "verification_code": "123456"})
        .with_html_template("verification.html", folder_name="verification")
        .with_text_template("verification.txt", folder_name="verification")
        .send()
    )
    return HttpResponse("Verification email sent!")
```

---

### 🔗 Step 6: Wire Up URLs

Create `core/urls.py`:

```python
from django.urls import path
from .views import test_email_view

urlpatterns = [
    path("send-verification-email/", test_email_view),
]
```

Then include it in `config/urls.py`:

```python

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

```

---

### 🚀 Step 7: Run and Test

```bash
python manage.py runserver
```

Open [http://localhost:8000/send-verification-email/](http://localhost:8000/send-verification-email/) in your browser and check your inbox!

---


## 💡 Tips

- You can subclass `EmailSender` for different email types or simply wrap it in functions.
- Organise your templates by email type (`registration/`, `verification/`, etc.)
- Subject and context are fully customisable.

---

## Advanced Usage

### Adding Multiple Recipients

To send an email to multiple recipients, you can pass a list of email addresses. If you want to add extra recipients dynamically, you can use the `add_new_recipient` method.

```python
# Add extra recipients using add_new_recipient
email_sender.add_new_recipient("extra_recipient@example.com")
.add_new_recipient("extra_recipient2@example.com")
.add_new_recipient("extra_recipient3@example.com")
.add_new_recipient("extra_recipient4@example.com")

# Send to all recipients

```

### Customising the Logger

You can configure the logger to output email logs to different destinations (such as a file or database) and apply custom formats to your logs.

#### Custom Formatter

You can add a custom formatter to modify how email logs are displayed. A custom formatter must be a callable function that accepts an `Exception` object (and optionally a traceback string) and returns a formatted string.

Here’s an example custom formatter:

```python
def custom_email_formatter(exc: Exception, trace: str = None) -> str:
    """
    Custom formatter that formats the exception message and traceback.
    """
    return f"Custom Error: {exc.__class__.__name__} - {exc.args[0]}.\nTraceback:\n{trace if trace else 'No traceback available'}"
```

To use this formatter with the `EmailSenderLogger` logger, set it as the custom formatter:

```python
email_sender.set_logger(custom_formatter=custom_email_formatter)
```

**Note:** Custom formatters should avoid using emojis or special characters like `->` in the output. Ensure your formatter returns a plain string that is suitable for logging.

### Logging to a File or Console

You can configure the logger to write email logs to a file, console, or both. Here's how to set up logging:

```python
import logging

# Set up logging to file
logging.basicConfig(filename='email_logs.log', level=logging.DEBUG)

# Or set up logging to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Add the handler to your email logger
email_sender._logger.addHandler(console_handler)
```

---

## Database Configuration

### Database Integration

`EmailSenderLogger` allows users to optionally persist email metadata to a database. This is useful for audit logs, diagnostics, and history tracking.

🔔 Note: `EmailSenderLogger` does not create or manage any database tables. You must define your own log model, and explicitly opt in to database logging.

`Requirements`:

> You must create your own model that inherits from EmailBaseLog.

> The model must be passed as a class, not an instance, using .add_log_model().

> You must explicitly enable database logging using .enable_email_meta_data_save().

> If no valid model is added, no data will be saved



### 📄 Example: Creating a Custom Email Log Model

```python

# models.py

from django_email_sender.models import EmailBaseLog 

class CustomEmailLog(EmailBaseLog):  # inherits from EmailBaseLog
    # Optional: Add custom fields
    request_id = models.CharField(max_length=100, null=True, blank=True)
    environment = models.CharField(max_length=20, default='production')

    def __str__(self):
        return f"{self.recipient} | {self.subject} | {self.status}"
```

`Run migrations`

```
python manage.py makemigrations
python manage.py migrate

```

`Note`:
The `EmailBaseLog` class is `an abstract model`, so it will not be created as a database table, even after running makemigrations and migrate.
Only your subclass (e.g., `CustomEmailLog`) will be created in the table and nothing else.


### 🛠️ Usage in Code

```python

from django_email_sender.email_logger import EmailSenderLogger
from "your-app".models import CustomEmailLog


email_sender = ( EmailSenderLogger.create().start_logging_session()
                .add_log_model(CustomEmailLog)    # customEmailLog
                .enable_email_meta_data_save()    # enable saving to the 
                
                # Rest of the code here .
                # .....
                .send()
)

```

## Clearing Fields

The `EmailSender` also provides methods to clear different email fields, such as `subject`, `from_email`, `to_email`, and more.

```python
# Clear specific fields
email_sender.clear_subject()
email_sender.clear_to_email()
email_sender.clear_html_template()
email_sender.clear_text_template()
```

If you want to clear all fields at once, use:

```python
email_sender.clear_all_fields()
```

These methods allow you to reset email properties, making it easier to send fresh emails with new details.

---

## Changelog

For the latest updates and changes, refer to the [Changelog](CHANGELOG.md).

---

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

This guide covers the core usage of the `django-email-sender` package, from setting up basic email functionality to advanced logging and database integration. For further customisation, refer to the documentation and adjust the settings to suit your project’s needs.
