# 📧 Django Email Sender Utility

A clean, reusable, lightweight and chainable utility class for sending emails in Django using templates. It supports both HTML and plain text templates, context injection, and flexible usage — either directly, via subclassing, or abstracted into functions.


## Table of Contents

- [📧 Why Use This?](#why-use-this)
- [✨ Features](#features)
- [🧼 Available Methods](#available-methods)
- [🧼 Code Style Tips](#code-style-tips)
- [🚀 Installation via PyPI](#installation-via-pypi)
- [🧩 Requirements](#requirements)
- [📧 HTML Email Template Example](#html-email-template-example)
- [📝 Plain Text & Multi-part Email Support](#plain-text--multi-part-email-support)
- [🧱 Subclassing](#subclassing)
- [🛠️ Function-Based Abstractions](#function-based-abstractions)
- [📁 Templates](#templates)
- [📁 Configuring the Template Directory](#configuring-the-template-directory)
- [🧩 Putting it all together Example](#putting-it-all-together)





## Why Use This? 

While Django already provides a way to send emails, it can become verbose and repetitive. `EmailSender` abstracts the boilerplate and lets you send templated emails fluently.

[🔝 Back to top](#table-of-contents)


## Features

- Chainable API (`.to()`, `.from_address()`, etc.)
- Supports HTML and plain text templates
- Uses Django's template system for dynamic content
- Easy to integrate and override
- Encourages clean code and reusability
- Supports subclassing or functional abstractions

[🔝 Back to top](#table-of-contents)

---


## Available Methods

Method	Description

```
  - create()                                                                                    
 - from_address(email)                                                                        
 - to(recipients)                                                                            
 - with_subject(subject)                                                                     
 - with_context(context)                                                                     
 - with_text_template(folder_name="folder-name-here", template_name="template-name-here.txt")  
 - with_html_template(folder_name="folder-name-here", template_name="template-name-here.html") 
 - with_headers(headers)                                                                     
 - send()
```
[🔝 Back to top](#table-of-contents)


🚨 Error Handling

```
 - Raises ValueError if required fields are missing.
 - Raises TypeError if headers are not provided as a dictionary.

```

## Code Style Tips

### 🔄 Formatting long method chains

When chaining multiple methods, breaking the chain onto separate lines can cause syntax errors unless you use an escape character (`\`). However, this approach can be difficult to read. A cleaner solution is to wrap the chain in parentheses.

#### 🔹 Using backslashes (`\`)

This works but can become harder to read as the chain grows:

```python
EmailSender.create()\
    .from_address(from_email)\
    .to([user.email])\
    .with_subject(subject)\
    .with_context({"username": user.username})\
    .with_text_template(text_registration_path, folder_name="emails")\
    .with_html_template(html_registration_path, folder_name="emails")\
    .send()
```

#### 🔹 Using parentheses (recommended)

This method is cleaner, more readable, and less error-prone:

```python

    EmailSender.create()
    .from_address(from_email)
    .to([user.email])
    .with_subject(subject)
    .with_context({"username": user.username})
    .with_text_template(text_registration_path, folder_name="emails")
    .with_html_template(html_registration_path, folder_name="emails")
    .send()

```
[🔝 Back to top](#table-of-contents)

---

## Installation via Pypi

[![PyPI version](https://badge.fury.io/py/django-email-sender.svg)](https://pypi.org/project/django-email-sender/)

django-email-sender is a Django package that allows you to send emails using customizable templates, with easy-to-use methods for setting the sender, recipients, subject, and context.

## Installation

To install the package:
```pip install django-email-sender ```


For more details, visit [the PyPI page](https://pypi.org/project/django-email-sender/).

[🔝 Back to top](#table-of-contents)


## Requirements

- Python 3.8+
- Django >= 3.2 < 6.0

## Compatibility

This package has been tested against Django 5.2 (the latest version at the time of release) and is known to work with versions 3.2 and above.

⚠️ **Compatibility with Django 6.x and beyond is not yet guaranteed.** If you're using a future version, proceed with caution and consider opening an issue if anything breaks.


[🔝 Back to top](#table-of-contents)

---


## HTML Email Template Example

`django-email-sender` supports sending beautiful HTML emails using Django templates.

This example shows a verification email template that you can use out of the box or modify to suit your needs.

🗂️ **Save this as**: `templates/emails_templates/emails/verify_email.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Verify Your Email</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 30px auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
        }
        .code {
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Verify Your Email Address</h1>
        <p>Hi {{ username }},</p>
        <p>Please verify your email address by entering the following code:</p>
        <div class="code">{{ verification_code }}</div>
        <p>If you didn't request this, you can safely ignore this email.</p>
    </div>
</body>
</html>
```

## Plain Text & Multi-part Email Support

`django-email-sender` supports both **plain text** and **multi-part (HTML + text)** emails. This ensures emails are readable in all clients, including those that don't support HTML.

---

### 📄 Plain Text Email Example

🗂️ **Save this as**: `templates/emails_templates/emails/verify_email.txt`

```txt
Hi {{ username }},

Please verify your email address by entering the following code:

{{ verification_code }}

If you didn't request this, you can safely ignore this email.

## Usage Example

```
📨  Multi-part Email (HTML + Plain Text) usage

Use both .with_text_template() and .with_html_template() together to send a multi-part email:

```
from django_email_sender import EmailSender

EmailSender.create()
    .from_address("noreply@example.com")
    .to(["user@example.com"])
    .with_subject("Please verify your email")
    .with_context({
        "username": user.username,
        "verification_code": "123456"
    })
    .with_html_template("verify_email.html", folder_name="emails")
    .with_text_template("verify_email.txt", folder_name="emails")
    .send()

```

✨ This approach helps you keep your email logic clean and makes templates easy to design or preview.


### Explanation:

- `.from_address("no-reply@example.com")`: Specifies the sender's email address.
- `.to(["recipient@example.com"])`       : Specifies the recipient's email address.
- `.with_subject("Welcome!")`            : The subject of the email.
- `.with_context({"username": "John"})`  : Context for the email templates, allowing dynamic insertion of values (e.g., the recipient's name).
- `.with_text_template("welcome.txt", folder_name="emails")`: The path to the text-based email template. Here, we specify the folder name (`emails`) where the template is stored. If no folder name is provided, it defaults to `email_templates/`.
- `.with_html_template("welcome.html", folder_name="emails")`: The path to the HTML-based email template. Similarly, you can specify the folder name (`emails`) for this template.
- `.send()`: Sends the email.

---

[🔝 Back to top](#table-of-contents)


## Subclassing

You can also subclass the `EmailSender` class to create more specific types of emails.

### Example: Password Reset Email

```python
class PasswordResetEmail(EmailSender):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def build(self):
        return self\
            .from_address("no-reply@example.com")\
            .to([self.user.email])\
            .with_subject("Reset Your Password")\
            .with_context({"username": self.user.username, "reset_link": generate_reset_link(self.user)})\
            .with_text_template("reset_password.txt", folder_name="emails")\
            .with_html_template("reset_password.html", folder_name="emails")
```

### Usage:

```python
PasswordResetEmail(user).build().send()
```

Here, the `PasswordResetEmail` class uses `reset_password.txt` and `reset_password.html` templates from the `emails` folder.

[🔝 Back to top](#table-of-contents)

---

## Function-Based Abstractions

🛠️ For a functional approach, you can also wrap `EmailSender` in specific functions to handle common email use cases.

### Example: Sending a Verification Email

```python

def send_verification_email(user):
    html_verification_path = "verification/verification.html"
    text_verification_path = "verification/verification.txt"
    subject = "Verify Your Email"
    from_email = "no-reply@example.com"

    return EmailSender.create()\
        .from_address(from_email)\
        .to([user.email])\
        .with_subject(subject)\
        .with_context({
            "username": user.username,
            "verification_link": generate_verification_link(user)
        })\
        .with_text_template(text_verification_path, folder_name="emails")\
        .with_html_template(html_verification_path, folder_name="emails")\
        .send()
```

### Example: Sending a Registration Email

```python
def send_registration_email(user):
    html_registration_path = "registration/registration.html"
    text_registration_path = "registration/registration.txt"
    
    subject = "Welcome to the Platform!"
    from_email = "no-reply@example.com"

    return EmailSender.create()\
        .from_address(from_email)\
        .to([user.email])\
        .with_subject(subject)\
        .with_context({"username": user.username})\
        .with_text_template(text_registration_path, folder_name="emails")\
        .with_html_template(html_registration_path, folder_name="emails")\
        .send()
```

### Advantages of this Approach:

- **Keeps your logic functional and simple**: It's straightforward to use and easy to test.
- **Keeps your email templates modular and easy to override**: Templates are organized in subfolders (e.g., `registration`, `verification`), making them easier to manage.
- **Clean and maintainable codebase**: You don’t have to subclass `EmailSender` each time, reducing complexity.


[🔝 Back to top](#table-of-contents)

---

## Templates

📁  Templates must reside inside a dedicated `email_templates/` directory, which should exist inside your Django template directory.

This folder can contain your own structure to help organise different types of emails. For example:

```
Example

project/
├── templates/
│   └── email_templates/
│       └── registration/
│           ├── registration.html
│           └── registration.txt
```

When calling `with_html_template()` or `with_text_template()`, you can provide the subfolder and filename like so:

```python
EmailSender.create()
    .with_html_template("registration.html", folder_name="registration")
    .with_text_template("registration.txt", folder_name="registration")
```

You **must** have both an `.html` and `.txt` version of the email template. These are required for rich content and email client compatibility.

[🔝 Back to top](#table-of-contents)

---


## Configuring the Template Directory**

📁 EmailSender allows you to easily configure the location of template directories used by the app, including email templates. By default, `EmailSender` will look for templates in a `templates` folder inside the base directory of your project. However, if you'd like to customize the location, you can do so using the `MYAPP_TEMPLATES_DIR` setting in your Django project's `settings.py`.

[🔝 Back to top](#table-of-contents)

---


## Default Behaviour

By default, EmailSender will look for templates in the following directory:

```
{BASE_DIR}/templates/emails_templates/
```

Where:
- `BASE_DIR` is the root directory of your Django project (where `manage.py` is located).
- `templates` is the default directory where EmailSender expects to find your templates.
- `emails_templates` is the subdirectory where email-related templates should be stored.

### Customizing the Template Directory Path

If you'd like to customize the template directory location, you can define the `MYAPP_TEMPLATES_DIR` setting in your `settings.py` file. 

### Steps to Override:

1. Open your `settings.py` file.
2. Define the `MYAPP_TEMPLATES_DIR` setting to point to your custom template folder.

#### Example:

```python
# settings.py

BASE_DIR = Path(__file__).resolve().parent.parent

# Custom template directory location
MYAPP_TEMPLATES_DIR = BASE_DIR / "custom_templates"
```

In this example:
- EmailSender will look for templates in `{BASE_DIR}/custom_templates/emails_templates/`.
- If you do not define `MYAPP_TEMPLATES_DIR`, EmailSender will use the default location: `{BASE_DIR}/templates/emails_templates/`.

[🔝 Back to top](#table-of-contents)

---

## **How It Works**

- **`MYAPP_TEMPLATES_DIR`**: If defined, EmailSender uses this setting to locate the main template folder.
- **Fallback**: If `MYAPP_TEMPLATES_DIR` is not defined, EmailSender falls back to the default location: `{BASE_DIR}/templates`.
- **Email Templates**: EmailSender looks specifically in the `emails_templates/` subdirectory for email-related templates.

### Example File Structure:

#### Default Setup:
```
my_project/
│
├── templates/
│   └── emails_templates/
│       └── welcome_email.html
```

#### Custom Setup (with `MYAPP_TEMPLATES_DIR` defined):
```
my_project/
│
├── custom_templates/
│   └── emails_templates/
│       └── welcome_email.html
```

[🔝 Back to top](#table-of-contents)

---

## **Error Handling**

If EmailSender cannot find the templates in the expected location, it will raise a `error` to let you know where the missing templates are expected.

If `BASE_DIR` is not defined in `settings.py`, an `ImproperlyConfigured` error will be raised to prompt you to define it.

[🔝 Back to top](#table-of-contents)

---

## **Fallback Logic**

In case the `MYAPP_TEMPLATES_DIR` is not defined in `settings.py`, EmailSender will automatically fallback to the default template directory (`templates`) without requiring any extra configuration.


### Conclusion

The `MYAPP_TEMPLATES_DIR` setting provides flexibility for users who prefer to store their templates in a custom location. By defining this setting in `settings.py`, users can control where the templates for EmailSender (including email templates) are stored, ensuring a smooth and configurable integration.

[🔝 Back to top](#table-of-contents)

---


## Putting It All Together

This guide shows how to use `django-email-sender` in a Django project to send a verification email.

---

### 🛠 Step 1: Virtual Environment

```bash
python -m venv venv
source venv/bin/activate.ps1
source venv/bin/activate      # On Mac or linux use: venv\Scripts\activate
```

---

### 📦 Step 2: Install Dependencies

```bash
pip install django django-email-sender
```

---

### ⚙️ Step 3: Create a Django Project

```bash
django-admin startproject config .
python manage.py startapp core
```

In `config/settings.py`, add `'core'` to `INSTALLED_APPS`.

---

### 🧱 Step 4: Update Django Settings
Add the following settings to your settings.py file to configure the email backend and other email-related settings.


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

- See `HTML Email Template Example` and `Plain Text & Multi-part Email Support`



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


## License
 - This package is licensed under the MIT License. See the LICENSE file for details.

## Credits
 -This project was created and maintained by Egbie Uku a.k.a EgbieAndersonUku1.

[🔝 Back to top](#table-of-contents)

