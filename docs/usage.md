# EmailSender Usage Guide

## Overview

`EmailSender` is a simple and flexible email-sending class designed to work seamlessly within the Django ecosystem, abstracting the boilerplate code needed to send templated emails. It allows for fluent method chaining and can be easily subclassed to create specific email-sending methods for your application.

---

## Installation

1. Install via `pip` from PyPi (or from your local package if you're working on development):

```bash
pip install emailsender
```

2. Make sure you have your Django project configured to send emails. In `settings.py`:

```python
EMAIL_USE_TLS = True  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587  
EMAIL_HOST_USER = 'your_email@gmail.com'  
EMAIL_HOST_PASSWORD = 'your_password'
```

---

## 📁 Templates

Make sure your templates exist in your Django template directory and follow the naming structure you define. Specifically, your **`email_templates`** folder should contain your email templates in the appropriate format for each type of email. Examples:

```
project/
├── templates/
│   └── email_templates/
│       └── registration/
│           ├── registration.html
│           └── registration.txt
```

---

## Basic Usage

### Sending a Simple Email

Here's how to send a simple email using `EmailSender`:

```python

from django_email_sender.email_sender import EmailSender

# Create the email sender instance
EmailSender.create()\
    .from_address("no-reply@example.com")\
    .to(["user1@example.com", "user2@example.com"])\  
    .with_subject("Welcome to the Platform!")\
    .with_context({"username": "Alice"})\
    .with_text_template("registration.txt", folder_name="registration")\
    .with_html_template("registration.html", folder_name="registration")\
    .send()
```

### Method Breakdown:

- `.from_address("email@example.com")`: Specifies the sender’s email address.
- `.to(["user@example.com"])`: Specifies the recipient(s), which can be a single email address or a list of addresses.
- `.with_subject("Your Subject")`: Specifies the subject of the email.
- `.with_context({"key": "value"})`: A dictionary of dynamic content for the email templates.
- `.with_text_template("template_name.txt", folder_name="folder_name")`: Path to the text-based email template. The `folder_name` refers to the subfolder within the `email_templates` directory where your template is stored. If no folder name is provided, it defaults to `email_templates/` in your template directory.
- `.with_html_template("template_name.html", folder_name="folder_name")`: Path to the HTML-based email template. Similar to `with_text_template`, the `folder_name` can be specified, and it defaults to `email_templates/` if not provided.
- `.send()`: Sends the email after all parameters are set.

---

## Advanced Usage

### Abstracting Email Logic into Specific Methods

To avoid repeating the same configuration for different types of emails (like registration, verification, etc.), you can abstract the `EmailSender` class into dedicated functions:

#### Example: Sending a Verification Email

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
        .with_text_template(text_verification_path, folder_name="verification")\
        .with_html_template(html_verification_path, folder_name="verification")\
        .send()
```

#### Example: Sending a Registration Email

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
        .with_text_template(text_registration_path, folder_name="registration")\
        .with_html_template(html_registration_path, folder_name="registration")\
        .send()
```

These methods can be expanded to include other types of emails (e.g., password reset, notifications, etc.), giving you a clean, consistent approach to email sending across your application.

---

## Subclassing `EmailSender`

You can easily subclass the `EmailSender` class to create specific types of emails. For example:

```python
class CustomEmailSender(EmailSender):
    def with_custom_header(self, custom_header):
        self.headers['X-Custom-Header'] = custom_header
        return self

    def send(self):
        # Custom send logic
        super().send()
```



## 🧱 Subclassing

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


```python
PasswordResetEmail(user).build().send()
```

Here, the `PasswordResetEmail` class uses `reset_password.txt` and `reset_password.html` templates from the `emails` folder.

---


You can then use this class in the same way:

```python
CustomEmailSender.create()\
    .from_address("no-reply@example.com")\
    .to(["user@example.com"])\  
    .with_subject("Custom Email")\
    .with_text_template("custom.txt", folder_name="custom")\
    .with_html_template("custom.html", folder_name="custom")\
    .with_custom_header("X-Custom-Value")\
    .send()
```

---

## Error Handling

The `send()` method will raise a `ValueError` if any of the essential email components are missing:

- `from_email`
- `to_email`
- `subject`
- `html_template`
- `text_template`

Make sure all required fields are set before calling `.send()`.

---

## Conclusion

The `EmailSender` class simplifies and streamlines email sending in Django projects, allowing for clean, readable, and reusable code. You can further extend it by creating specific email-sending functions or even subclassing it for custom behaviour. This ensures your email-related code remains flexible and maintainable.

---
