
[![Downloads](https://static.pepy.tech/badge/django-email-sender)](https://pepy.tech/project/django-email-sender)
[![PyPI version](https://img.shields.io/pypi/v/django-email-sender/2.0.0.svg?color=blue)](https://pypi.org/project/django-email-sender/2.0.0/)


# 📧 Django Email Sender Version 2

Django Email Sender is a lightweight and highly customisable utility for sending emails in Django using rich templates and a clean, chainable API.

---

## 🚀 What's New in v2.0

Version 2.0 brings powerful new features that make your email workflows smarter and more robust:

- ✅ **Email Delivery Tracking**  
  Get immediate feedback on whether an email was sent successfully or failed, with access to error messages if something goes wrong.

- 🔁 **Field Management (Preserve/Clear)**  
  Fine-grained control over email fields—clear or preserve specific fields even after setting them.

- 📝 **Logging and Database Integration**  
  Easily hook into your logging system to record email activity—log to file, console, or even a database.


- 🔧 **New method introduced to Chainable API**  
  Enhanced method chaining to improve developer ergonomics and reduce boilerplate.

---

## ✨ Features

- Rich HTML and plain text templates  
- Chainable email building methods  
- Custom function to format your logging
- Additional methods for fine grain control (v2.0+)
- Logging and database integration (v2.0+)  
- i18n support (v2.0+)

---

## 🧾 Changelog

### v2.0

- Added support for logging (file/database)  
- Added delivery status tracking with error feedback  
- Introduced methods to clear or preserve fields dynamically  
- Improved documentation and method chaining flexibility
- Ability to get metadata for a sent email
- See you payload before or after your email has been set
- and so much more


It provides a clean, reusable, and chainable utility class for sending emails in Django, supporting both HTML and plain text templates, dynamic context injection, and flexible usage — whether used directly, via subclassing, or abstracted into functions.


## Table of Contents

- [📧 Why Use This?](#why-use-this)
- [🔄 Upgrading from Version 1](#upgrading-from-version-1)
- [🆕 What's New in Version 2?](#what-is-new-in-version-2)
- [✨ Features](#features)
- [🔄 What is `EmailSender` and what is `EmailSenderLogger`, and why are they needed?](#what-is-emailsender-and-what-is-emailsenderlogger-and-why-are-they-needed)
- [🤔 What if I am not interested in using the advanced features provided by `EmailSenderLogger`?](#what-if-i-am-not-interested-in-using-the-advanced-features-provided-by-emailsenderlogger)
- [📧 `EmailSender` Class API Reference](#emailsender-class-api-reference)
- [📝 `EmailSenderLogger` Class API Reference](#emailsenderlogger-class-api-reference)
- [🧼 Available Methods](#available-methods)
- [🔄 Additional API Notes](#additional-api-notes)
- [🧩`EmailSender` and `EmailSenderLogger` Methods](#emailsender-and-emailsenderlogger-methods)
- [🧼 Code Style Tips](#code-style-tips)
- [🚀 Installation via PyPI](#installation-via-pypi)
- [🧩 Requirements](#requirements)
- [📝 Logger and Database Integration](#logger-and-database-integration)
- [📝 How to configure the Logger](#how-to-configure-the-logger)
- [🛠️ Example Setting up a simple Logger with EmailSenderLogger](#example-setting-up-a-simple-logger-with-emailsenderlogger)
- [🔁 Reuse the Logger and Formatter Across Multiple Emails](#reuse-the-logger-and-formatter-across-multiple-emails)
- [🗣️ Turning on Verbose Mode](#turning-on-verbose-mode)
- [🧭 Tracing Method Chains and logging errors with `set_traceback`](#tracing-method-chains-and-logging-errors-with-set_traceback)
- [⚙️ Setting up an advanced logger](#setting-up-an-advanced-logger)
- [🔄 Advanced Tip: Rotate Log Files Automatically](#advanced-tip-rotate-log-files-automatically)
- [📈 Advanced Logger Usage](#advanced-logger-usage)
- [🗃️ Database Integration](#database-integration)
- [📝🔒 Logger](#logger)
- [🛠️ Setting up the logger ](#example-setting-up-a-logger-with-emailsender)
- [🛠️ Setting up an advanced logger](#setting-up-an-advanced-logger)
- [📝 Reuse the Logger and Formatter Across Multiple Emails](#reuse-the-logger-and-formatter-across-multiple-emails)
- [🔄 Resetting or Reusing the Instance Cleanly](#resetting-or-reusing-the-instance-cleanly)
- [📧 HTML Email Template Example](#html-email-template-example)
- [📝 Plain Text & Multi-part Email Support](#plain-text--multi-part-email-support)
- [🧱 Subclassing](#subclassing)
- [🛠️ Function-Based Abstractions](#function-based-abstractions)
- [📁 Templates](#templates)
- [📁 Configuring the Template Directory](#configuring-the-template-directory)
- [🌐 Multilingual Error Messages](#multilingual-error-messages)
- [🧩 Putting it all together Example](#putting-it-all-together)
- [🎮 Playing Around with Features Without Sending Emails](#playing-around-with-features-without-sending-emails)
- [🏆 Best Practices](#best-practices)
- [❌ Worst Practices](#best-practices)



## Why Use This? 

While Django already provides a way to send emails, it can become verbose and repetitive. `EmailSender` abstracts the boilerplate and lets you send templated emails fluently.

[🔝 Back to top](#table-of-contents)


## 🔄 Upgrading from Version 1

Version 2 introduces powerful new features — with **zero breaking changes**. Your current integration will continue to work as expected!

### 🚀 What’s New in v2:

- ✅ **Integrated Logging & Database Support**  
  Log email activity to a file or database with customisable logging levels (`debug`, `info`, `warning`, `error`).

- 🧼 **Advanced Field Management**  
  - Auto-reset fields after sending  
  - Clear specific fields or all fields  
  - Preserve chosen fields across sends

- 📋 **Selective Logging with Inclusion/Exclusion Rules**  
  Choose exactly which fields to log (`log only`) and which to exclude (`log exclude`) — giving you full control over what gets logged.

- 📊 **Custom Log Range**  
  Define a log range to specify precisely what data is captured in logs, improving privacy and debugging clarity.

- 🧠 **Smarter Error Handling**  
  Now with field-level and error messages for easier debugging and localisation.

---

**✅ No breaking changes** — Drop-in upgrade, full backwards compatibility.

## 📦 What’s New in Version 2?

Version 2 of Django Email Sender brings major upgrades while maintaining full backwards compatibility. It’s smarter, more flexible, and much more powerful.

- 📝 **Custom Logger Integration**  
  - Plug in your own logger for full control over log output and formatting.  
  - Easily inherit from the base abstract model to create a custom log model.  
  - Save logs to the database or file via the `EmailLogger` integration.

- 🔄 **Auto-Reset After Sending**  
  Automatically reset all email fields after sending with `auto_reset=True` to prevent accidental resends.

- 📌 **Preserve Specific Fields**  
  Use `preserve_fields` to retain selected fields even after an auto-reset.

- 🧼 **Individual Field Clearing**  
  Clear only what you need with new methods like `clear_subject()`, `clear_context()`, `clear_to()`, and more.

- ⚙️ **Inclusion/Exclusion Logging**  
  Choose exactly which fields to log (`log_only`) and which to exclude (`log_exclude`) for fine-grained control.

- 📊 **Custom Log Range**  
  Define a logging range to specify precisely what data is logged, improving privacy and audit clarity.


- 🗂 **EmailSenderLogger Class**  
  A dedicated logger class to manage logging behaviour, output types, and integration points.

- 🧰 **More Utility Methods**  
  Version 2 introduces several new helper methods to simplify template handling, payload inspection, metadata access, and more.  
  _Check the full documentation for all available methods and usage examples._


## ✨ Features

- 🛠️ **Custom logger integration**  
  Plug in your own logger for full control over log formatting and output. Easily log email activities to files or databases.

- 🗂️ **Database logging support**  
  Integrate email logs directly into your database via the `EmailLogger`, with easy-to-configure log models.

- 🔗 **Chainable API**  
  Fluent, easy-to-use API for configuring email attributes — e.g., `.to()`, `.from_address()`, `.subject()`, `.context()`, etc.

- 🔄 **Auto-reset**  
  Automatically reset all fields after sending an email, keeping your instance clean for reuse.

- 🧼 **Field clearing and preservation**  
  Clear individual fields (e.g., subject, recipients, templates) or preserve them between email sends.

- 🧼 **logging including inclusion/exclusion**  
 Chose what fields you would like to log (e.g., subject, recipients, templates) 

- 📨 **HTML and plain text templates**  
  Send both HTML and plain-text emails with rich template support for flexibility.

- 🧩 **Lightweight & easy integration**  
  Simple to integrate into any Django project without unnecessary complexity.

- 🧱 **Clean architecture & folder structure**  
  Encourages good code practices with reusable components and clear folder organization.

- 🧬 **Subclassing & functional abstractions**  
  Extensible through subclassing or functional abstractions for maximum flexibility.

- 🧪 **Testable and extendable**  
  Designed with testability in mind, making it easy to write unit and integration tests.




[🔝 Back to top](#table-of-contents)

---


### Sample Code Comparison: Version 1 vs Version 2

**Version 1 (Classic Usage)**

```python

# Without auto-reset and custom logger (classic usage)
from django_email_sender.email_sender import EmailSender
  (
   EmailSender.create() 
    .from_address("no-reply@example.com") 
    .to(["test@example.com"]) 
    .with_subject("Welcome Email") 
    .with_context({"username": "John"}) 
    .with_html_template("welcome.html", folder_name="welcome") 
    .with_text_template("welcome.txt", folder_name="welcome") 
    .send()
  )

```

### 🚀 Version 2 — Demo: Custom Logger & Database Logging
```python
## 

```python
import logging

from django_email_sender.email_sender import EmailSender
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.email_sender_constants import LoggerType, EmailSenderConstants

# For database logging, import your custom model inheriting from EmailBaseLog:
from <your_app>.models import YourCustomEmailLog


# ---------------------------
# Example: models.py
# ---------------------------
from django.db import models
from django_email_sender.models import EmailBaseLog

class YourCustomEmailLog(EmailBaseLog):
    # You can add any custom fields or methods if needed
    pass


# ---------------------------
# Example: views.py
# ---------------------------

# Optional: custom formatter for logger messages
def my_custom_formatter(exception: Exception, trace: str) -> str:
    return f"[CUSTOM ERROR] {str(exception)} | Trace: {trace}"


# Set up your own logger
logger = logging.getLogger("email_sender")

# Start the logging session
email_sender = (
    EmailSenderLogger.create()
    .start_logging_session()
    .enable_verbose()                                    # Enables verbose output for detailed logging
    .config_logger(logger, LoggerType.DEBUG)             # Plug in your custom logger
    .add_email_sender_instance(EmailSender.create())     # Attach the EmailSender instance
    .add_log_model(YourCustomEmailLog)                   # Use your custom DB model for logs
    .enable_email_meta_data_save()                       # Enable to save to db
    .from_address("no-reply@example.com")
    .to("jackie@example.com")
    .add_new_recipient("mj@example.com")
    .add_new_recipient("ba@example.com")
    .add_new_recipient("eu@gmail.com")
    .add_new_recipient("scott_mccall@example.com")
    .with_context({"promo_code": "12345"})
    .with_subject("Promo code for our loyal customers")
    .with_html_template("test_email.html", "sender")
    .with_text_template("test_email.txt", "sender")
    .send()
)

# Access the payload (for debugging or logging)
payload = email_sender.payload

# Access email meta-data (headers, timestamps, etc.)
meta_data = email_sender.email_meta_data

```
✅ Notes:

> Make sure your logger is configured in settings.py.

> Your custom model must inherit from EmailBaseLog.

> You can override or extend the base model with your own fields.

💡 Tip:

This is just a basic example — additional configuration options like preserve_fields, auto_reset, clear_*() methods, etc. See the documentation for details


### 📝 Minimal Example — Custom Logger Only (No DB Integration)

 A minimal example that shows off just the custom logging integration without the database part. This is great for users who want to plug in a logger quickly without setting up a database model.


 ```python
 import logging

from django_email_sender.email_sender import EmailSender
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.email_sender_constants import LoggerType

# Optional: custom formatter for your log output
def my_custom_formatter(exception: Exception, trace: str) -> str:
    return f"[CUSTOM LOG] {str(exception)} | Traceback: {trace}"

# Set up your logger (must be configured in Django settings)
logger = logging.getLogger("email_sender")

# Start logging session
email_sender = (
    EmailSenderLogger.create()
    .start_logging_session()
    .enable_verbose()                  # Verbose logging for detailed trace
    .config_logger(logger, LoggerType.INFO)
    .set_custom_formatter(my_custom_formatter)
    .add_email_sender_instance(EmailSender.create())
    .from_address("noreply@example.com")
    .to("user@example.com")
    .with_subject("Welcome!")
    .with_html_template("emails/welcome.html", "sender")
    .with_text_template("emails/welcome.txt", "sender")
    .send()
)

# Optionally access logging details
print(email_sender.payload)
print(email_sender.email_meta_data)

```
⚡ Highlights

> No custom model setup required.

> Plug-and-play logging with any Python logger.

> Add your own formatter to control log message output.

> Great for development or production environments where full DB logging isn’t needed.


## What is `EmailSender` and what is `EmailSenderLogger`, and why are they needed?

`EmailSender` is a module that allows you to send customisable emails with rich templates. It abstracts the multiple steps needed to send an email and enables you to do so in a quick, easy, and chainable manner.

While `EmailSender` does support sending emails, it lacks several functionalities:

- No tracking of the sending process, making debugging difficult
- No logging capabilities
- No visibility of payloads (pre-send or post-send)
- No access to metadata
- No database interaction
- No delivery tracking

### Why is `EmailSenderLogger` needed?

Although `EmailSender` has recently been upgraded with new features—such as clearing specific fields, resetting values, and preserving data after sending—it still focuses solely on sending emails. As a result, it doesn’t provide methods to track or log email operations.

This is where `EmailSenderLogger` comes in.

It’s a lightweight wrapper that extends `EmailSender` with powerful features:

- Integrated logging support
- Optional database logging
- Email report summaries (e.g., sent vs not sent)
- Real-time access to the email payload during construction
- Full metadata retrieval after the email is sent
- Preview support for both HTML and plain text templates
- And much more

⚠️ Note: `EmailSenderLogger` does **not** include a logger or database by default. You must inject these via the provided public methods.

If you choose not to supply a logger or database, that’s fine—`EmailSenderLogger` will still work, inheriting all functionality from `EmailSender`.

To use it, simply power `EmailSenderLogger` with an instance of `EmailSender`:

```python
email_sender = (
    EmailSenderLogger.create()
        .add_email_sender_instance(EmailSender.create()) # must be powered by the instance of EmailSender
        .from_address("noreply@example.com")
        .to("user@example.com")
        .with_subject("Welcome!")

        # rest of the chain here
        # ...
        .send()
)

# do something with `email_sender` if you want
```
---

[🔝 Back to top](#table-of-contents)

### What if I’m not using the advanced features of `EmailSenderLogger`?

That’s completely fine. If you don’t require logging or database integration, you can continue using `EmailSender` directly.

However, `EmailSenderLogger` is a subclass of `EmailSender`, meaning it fully supports all core email-sending features. If you prefer to use `EmailSenderLogger` (e.g., for future extensibility), simply initialise it with an instance of `EmailSender`.

```python
logger = EmailSenderLogger.create().add_email_sender_instance(EmailSender.create() or EmailSender())
```

Unless you explicitly opt-in to the enhanced features (e.g., by starting a logging session), `EmailSenderLogger` behaves just like `EmailSender`.

---


[🔝 Back to top](#table-of-contents)


## Available Methods

Method Description

### EmailSender methods
```markdown

 - create()                                                                                    
 - from_address(email)                                                                        
 - to(recipients)                                                                            
 - with_subject(subject)                                                                     
 - with_context(context)                                                                     
 - with_text_template(folder_name="folder-name-here", template_name="template-name-here.txt")  
 - with_html_template(folder_name="folder-name-here", template_name="template-name-here.html") 
 - with_headers(headers) 
 - clear_from_email()       #  Added in version 2 
 - clear_to_email()         #  Added in version 2 
 - clear_subject()          #  Added in version 2 
 - clear_context()          #  Added in version 2 
 - clear_to_email()         #  Added in version 2 
 - clear_html_template()    #  Added in version 2     
 - clear_text_template()    #  Added in Version 2     
 - clear_from_email()       #  Added in Version 2 
 - clear_all_fields()       #  Added in Version 2                                   
 - send()
```

[🔝 Back to top](#table-of-contents)


### `EmailSender` Class API Reference

#### 🔨 `create()`
> **Factory method** — Instantiates and returns an `EmailSender` object.

#### 📤 `from_address(email)`
> **Sets the sender's email address**.  
> `email`: A string representing the sender's email (e.g. `noreply@yourdomain.com`).

#### 📥 `to(recipients)`
> **Sets the recipient(s) of the email**.  
> `recipients`: A string or list of strings with one or more email addresses.

#### 📝 `with_subject(subject)`
> **Sets the subject line of the email**.  
> `subject`: A string for the email's subject.

#### 🔧 `with_context(context)`
> **Provides the context dictionary for rendering templates**.  
> `context`: Optional. A dictionary containing variables that can be used in both HTML and text templates. This method is only necessary if your templates require dynamic content (variables) to be rendered.

#### 📄 `with_text_template(folder_name="folder-name-here", template_name="template-name-here.txt")`
> **Specifies the plain text template**.  
> If `folder_name` is omitted, defaults to `emails_templates/`.

#### 🌐 `with_html_template(folder_name="folder-name-here", template_name="template-name-here.html")`
> **Specifies the HTML version of the email template**.  
> If `folder_name` is omitted, defaults to `emails_templates/`.

#### 🧾 `with_headers(headers)`
> **Optional method to add custom email headers**.  
> `headers`: A dictionary of headers (e.g. `{"X-Custom-Header": "value"}`).

#### ✂️ `clear_subject()`
> Clears the subject field to its default empty value. This method is optional and can be called as part of a method chain.  It's only relevant if the object has been instantiated and used as a chain. Calling this method clears the subject field without affecting other fields in the chain.

```python
    from django_email_sender.email_sender import EmailSender

    # instantialize the Email sender
    email_sender = EmailSender.create()

    email_sender.from_address(from_email)
                .to([user.email])
                    .with_subject(subject)
                    .with_context({"username": 'John'})
                    .with_text_template(text_registration_path, folder_name="emails")
                    .with_html_template(html_registration_path, folder_name="emails")
                    .send()
                    .clear_subject() # Clears the subject field from the chain

   # or it can be cleared directly from the instant method
   email_sender.clear_subject()
```

#### 🧳 `clear_context()`
**New in version 2.** 
> Clears the context field to its default empty value. This method is optional and can be called as part of a method chain. It's only relevant if the object has been instantiated and used as a chain. Calling this method clears the context field without affecting other fields in the chain

```python
    from django_email_sender.email_sender import EmailSender

    # instantialize the Email sender
    email_sender = EmailSender.create()

    email_sender.from_address(from_email)
                .to([user.email])
                    .with_subject(subject)
                    .with_context({"username": 'John'})
                    .with_text_template(text_registration_path, folder_name="emails")
                    .with_html_template(html_registration_path, folder_name="emails")
                    .send()
                    .clear_context()  # Clears the context field from the chain

   # or it can be cleared directly from the instant method
   email_sender.clear_context()  # Clears the context field from the chain
```

#### 📨 `clear_to_email()`
**New in version 2.** 
> Clears the recipient field to its default empty value. This method is optional and can be called as part of a method chain. It's only relevant if the object has been instantiated and used as a chain. Calling this method clears the recipient field without affecting other fields in the chain.

```python
    from django_email_sender.email_sender import EmailSender

    # instantialize the Email sender
    email_sender = EmailSender.create()

    email_sender.from_address(from_email)
                .to([user.email])
                    .with_subject(subject)
                    .with_context({"username": 'John'})
                    .with_text_template(text_registration_path, folder_name="emails")
                    .with_html_template(html_registration_path, folder_name="emails")
                    .send()
                    .clear_to_email()  # Clears the recipient field from the chain


   # or it can be cleared directly from the instant method
  email_sender.clear_to_email()
```

#### 📨 `clear_from_email()`
**New in version 2.** 
> Clears the sender email field to its default empty value. This method is optional and can be called as part of a method chain. It's only relevant if the object has been instantiated and used as a chain. Calling this method clears the sender email field without affecting other fields in the chain

```python
    from django_email_sender.email_sender import EmailSender

    # instantialize the Email sender
    email_sender = EmailSender.create()

    email_sender.from_address(from_email)
                .to([user.email])
                    .with_subject(subject)
                    .with_context({"username": 'John'})
                    .with_text_template(text_registration_path, folder_name="emails")
                    .with_html_template(html_registration_path, folder_name="emails")
                    .send()
                    .clear_from_email()  # Clears the sender email field from the chain


   # or it can be cleared directly from the instant method
  email_sender.clear_from_email()
```

#### 🧑‍💻 `clear_html_template()`
**New in version 2.** 
> Clears the HTML template field to its default empty value. This method is optional and can be called as part of a method chain. It's only relevant if the object has been instantiated and used as a chain. Calling this method clears the HTML template field without affecting other fields in the chain.


```python
    from django_email_sender.email_sender import EmailSender

    # instantialize the Email sender
    email_sender = EmailSender.create()

    email_sender.from_address(from_email)
                .to([user.email])
                    .with_subject(subject)
                    .with_context({"username": 'John'})
                    .with_text_template(text_registration_path, folder_name="emails")
                    .with_html_template(html_registration_path, folder_name="emails")
                    .send()
                    .clear_html_template()  # Clears the HTML template field from the chain


   # or it can be cleared directly from the instant method
  email_sender.clear_html_template()  
```

#### 📝 `clear_text_template()`
**New in version 2.** 
> Clears the text template field to its default empty value. This method is optional and can be called as part of a method chain. It's only relevant if the object has been instantiated and used as a chain. Calling this method clears the text template field without affecting other fields in the chain.


```python
    from django_email_sender.email_sender import EmailSender

    # instantialize the Email sender
    email_sender = EmailSender.create()

    email_sender.from_address(from_email)
                .to([user.email])
                    .with_subject(subject)
                    .with_context({"username": 'John'})
                    .with_text_template(text_registration_path, folder_name="emails")
                    .with_html_template(html_registration_path, folder_name="emails")
                    .send()
                    .clear_text_template()  # Clears the text template field from the chain


   # or it can be cleared directly from the instant method
  email_sender.clear_text_template() 
```


#### 🔄 `clear_all_fields()`
**New in version 2.** 
>Clears all fields to their default empty values. This method is optional and can be called as part of a method chain. It's only relevant if the object has been instantiated and used as a chain. Calling this method clears all fields without affecting the rest of the method chain or the logger if added.


```python
    from django_email_sender.email_sender import EmailSender

    # instantialize the Email sender
    email_sender = (
            
        EmailSender.create()
        email_sender.from_address(from_email)
                    .to([user.email])
                        .with_subject(subject)
                        .with_context({"username": 'John'})
                        .with_text_template(text_registration_path, folder_name="emails")
                        .with_html_template(html_registration_path, folder_name="emails")
                        .send()
                        .clear_all_fields()  # Clears all fields in the chain without but leaves fields like logger, etc intact
    )

   # or it can be cleared directly from the instant method
  email_sender.clear_all_fields()   
```

#### 📬 `send(auto_reset=False)`

> **Sends the email** using the provided configuration and templates.

> **Optional parameters** 
  **New in version 2.** 
> > **auto_reset** If set to True, all fields will be cleared after the email is sent. Default is False.`

---

[🔝 Back to top](#table-of-contents)


###  `EmailSenderLogger` Class API Reference

### 🔨 `create()`
> **Factory method** — Instantiates and returns an `EmailSenderLogger` object.

---

#### 📤 `add_email_sender_instance(email_sender_instance)`
> Sets the core `EmailSender` instance that will be used to send emails.

---

#### 📥 `to(recipients)`
> The ability to add multiple recipients via a list has been **removed** and **replaced** with `add_new_recipient`.  
> This method now only accepts a string. To add multiple recipients use `add_new_recipient` method 

---

#### 📥 `add_new_recipient(recipient)`
> **New in version 2.**  
> Accepts a string and adds it to the set of recipients. To add multiple recipients, call this method repeatedly. The method uses a set to ensure that recipient names are unique.


---

#### 📝 `with_subject(subject)`
> Sets the subject line of the email.

---

#### 🔧 `with_context(context)`
> Sets the context dictionary for dynamic rendering of email templates.

---

#### 📄 `with_text_template(folder_name, template_name)`
> Specifies the plain text template to use.  
> If `folder_name` is omitted, defaults to `emails_templates/`.

---

#### 🌐 `with_html_template(folder_name, template_name)`
> Specifies the HTML version of the email template.  
> If `folder_name` is omitted, defaults to `emails_templates/`.

---

#### 📑 `with_headers(headers)`
> Optional method to add custom email headers (as a dictionary).

---

#### 🧩 `set_custom_formatter(custom_formatter)`
> Adds a custom error formatter to customise how exceptions and traces are logged.

---

#### 🛠 `config_logger(logger: Logger, log_level: LoggerType)`
> Integrates an external Python logger and sets its log level.
---

#### Logger Configuration

🧾 To customise how and at what level email sending is logged, use the `config_logger()`. The levels can be added manually or used with `LoggerType` constants provided. 


```python

  from django_email_sender.email_sender_constants import LoggerType

  email_logger.config_logger(my_logger, LoggerType.INFO)

```

 | Constant           | Description                              |
|--------------------|------------------------------------------|
| `LoggerType.INFO`  | Standard informational messages           |
| `LoggerType.WARNING` | Non-critical issues worth noting        |
| `LoggerType.ERROR` | Errors encountered during sending         |
| `LoggerType.DEBUG` | Verbose output for development/debugging |



---

#### 🗃 `add_log_model(log_model: EmailBaseLog)`
> Attaches a custom model for database email logging.  
> The model provided must inherit from the `abstract` base model `EmailBaseLog`
> The module path : `from django_email_sender.models import EmailBaseLog`

---

#### 🧪 `to_debug(message)`
> Logs a message at the `DEBUG` level.

---

#### ℹ️ `to_info(message)`
> Logs a message at the `INFO` level.

---

#### ⚠️ `to_warning(message)`
> Logs a message at the `WARNING` level.

---

#### ❌ `to_error(message)`
> Logs a message at the `ERROR` level.

---

#### 🔊 `enable_verbose()`
> Enables verbose logging (e.g., shows additional trace and context information).

---

#### 🔇 `disable_verbose()`
> Disables verbose mode and limits logs to essential information.

---
### Logging Control Methods

Use the following methods to manage logging dynamically during the email sending flow.

#### [`start_logging_session()`](#start_logging_session) 🔓  
> Starts the logging session and returns `self` for chaining.  
> Useful if you want to enable logging partway through your workflow.  
>  
> **Note:** If a logger has been added, you **must** call this method — otherwise, no information will be logged, and you’ll see the following output in your logs:

```plaintext
[2025-05-10 17:41:37,136] DEBUG    email_sender : [Logger Not Enabled: Logger is not enabled. Skipping logging. | category=LOGGER | status=NOT_ENABLED]
[2025-05-10 17:41:37,136] DEBUG    email_sender : [Logger Not Enabled: Logger is not enabled. Skipping logging. | category=LOGGER | status=NOT_ENABLED]
[2025-05-10 17:41:37,136] DEBUG    email_sender : [Logger Not Enabled: Logger is not enabled. Skipping logging. | category=LOGGER | status=NOT_ENABLED]
[2025-05-10 17:41:37,136] DEBUG    email_sender : [Logger Not Enabled: Logger is not enabled. Skipping logging. | category=LOGGER | status=NOT_ENABLED]

```

---

#### [`stop_logging_session()`](#stop_logging_session) 🔒  
> Completely disables further logging and ends the session.

---

#### [`pause_logging()`](#pause_logging) ⏸️  
> Temporarily pauses logging without clearing state.

---

#### [`resume_logging()`](#resume_logging) ▶️  
> Resumes logging after a `pause_logging()` call.


#### 📬 `is_email_sent` (Property)
> Returns `True` if the last email was successfully sent, otherwise `False`.

---

#### 🔢 `email_delivery_count` (Property)
> Returns the number of successfully delivered emails in the current session.

---

#### 📦 `payload` (Property)
> Returns the email payload dictionary. Useful for auditing and testing.

---

#### 🧾 `email_meta_data` (Property)
> Returns meta information such as timestamps, recipients, and status.

---

#### 🧮 `return_successful_payload()` (Not chainable)
> Returns a *copy* of the `_field_changes` dictionary, which logs what fields were changed and when.  
> This ensures the original audit trail remains unmodified.

---

### 🧠 set_traceback(show_traceback: bool, method_tracing: bool = False )
> method_tracing: show exactly which methods were called during your email building process, `set_traceback()` is your friend. It provides a step-by-step breakdown of the chained method calls that lead up to sending an email. Note, this must be set to `True`, default is `False`
> show_traceback: shows you a traceback error including the point where the error originated.
   
---    

#### 🛑 `log_only_fields(*fields)`
> Restricts logging to specific fields (e.g., only `subject` or `to`).  
> Useful for minimising log verbosity.

---

#### 🚫 `exclude_fields_from_logging(*fields)`
> Excludes specific fields from being logged, even if logging is enabled.

---

#### 🔄 `reset_field_logging_filters()`
> Clears all field-based filters (`log_only_fields` and `exclude_fields_from_logging`) and resets to default logging behaviour.

---

#### 🧠 `enable_email_meta_data_save(save_to_db=True)`
> Enables metadata saving for each email sent. If `save_to_db=True`, the metadata will also be saved to the database via the configured model.

### 🧠 return_successful_payload()
>  Returns the email payload for logging, but only if the email was successfully processed.


[🔝 Back to top](#table-of-contents)


## Additional API Notes

### 🔁 Shared Methods Between `EmailSenderLogger` and `EmailSender`

📎 Since `EmailSenderLogger` is a wrapper around `EmailSender`, it inherits many of the same methods. For more detailed explanations, refer to the [EmailSender API](#emailsender-class-api-reference) section.

##  Using Model Constants to Minimise Errors

📨 To reduce the risk of typos and improve code clarity, both `EmailSender` and `EmailSenderLogger` support the use of constants via the `EmailSenderConstants` enum.

Instead of hardcoding strings like `"from_email"` or `"subject"` when specifying fields, use the enums for safer, auto-completable references.

⚠️ **Note:** These enums must be used with `.value`, as they are instances of `Enum`. This can then be passed in
`methods` like `exclude_fields_from_logging` or `log_until_field` 

---

### `EmailSenderConstants` Fields 🔠


| Constant                               | Field Name           | Description                                        |
|----------------------------------------|----------------------|----------------------------------------------------|
| `EmailSenderConstants.Fields.FROM_EMAIL`        | `"from_email"`       | The sender's email address                         |
| `EmailSenderConstants.Fields.TO_EMAIL`          | `"to_email"`         | The recipient's email address                      |
| `EmailSenderConstants.Fields.SUBJECT`           | `"subject"`          | The subject line of the email                      |
| `EmailSenderConstants.Fields.HTML_TEMPLATE`     | `"html_template"`    | The HTML template used to render the email body    |
| `EmailSenderConstants.Fields.TEXT_TEMPLATE`     | `"text_template"`    | The plain text version of the email body           |
| `EmailSenderConstants.Fields.CONTEXT`           | `"context"`          | A dictionary of variables used in template rendering |
| `EmailSenderConstants.Fields.HEADERS`           | `"headers"`          | Optional custom email headers                      |
| `EmailSenderConstants.Fields.LIST_OF_RECIPIENT` | `"list_of_recipients"` | A list of recipient email addresses             |
| `EmailSenderConstants.Fields.EMAIL_ID`          | `"email_id"`         | Unique identifier for the email instance           |


📊 Logging-specific use (with EmailSenderLogger)

```python
from django_email_sender.email_sender_constants import EmailSenderConstants

email_sender_with_logging = EmailSenderLogger.create().start_logging_session()
email_sender_with_logging.exclude_fields_from_logging(
    EmailSenderConstants.Fields.CONTEXT.value,
    EmailSenderConstants.Fields.HEADERS.value,
)

```


📩 Non-logging use (with EmailSender)
```python

from django_email_sender.email_sender_constants import EmailSenderConstants

email_sender = EmailSender.create()
email_sender.send(
    auto_reset=True,
    preserve_fields=[
        EmailSenderConstants.Fields.CONTEXT.value,
        EmailSenderConstants.Fields.SUBJECT.value
    ]
)

```
This approach ensures consistency across your codebase and provides a single source of truth for all field and method references related to EmailSender and EmailSenderLogger.= "add_new_recipient"


[🔝 Back to top](#table-of-contents)

###  `EmailSender` and `EmailSenderLogger` Methods

#### **Core Functions**

| Name                           | Type    | Chainable | Description                                      | Defined In           |
|---------------------------------|---------|-----------|--------------------------------------------------|----------------------|
| `create()`                     | Method  | ✅         | Factory method to instantiate the class          | Both                 |
| `to(recipients)`               | Method  | ✅         | Set recipient(s)                                 | Both                 |
| `with_subject(subject)`        | Method  | ✅         | Set the subject of the email                     | Both                 |
| `with_context(context)`        | Method  | ✅         | Set template context                             | Both                 |
| `with_text_template(...)`      | Method  | ✅         | Attach plain text template                       | Both                 |
| `with_html_template(...)`      | Method  | ✅         | Attach HTML template                             | Both                 |
| `with_headers(headers)`        | Method  | ✅         | Add custom headers                               | Both                 |
| `send(auto_reset=False, ...)`  | Method  | ❌         | Sends the email                                  | Both                 |
| `clear_subject()`              | Method  | ✅         | Clears the subject field                         | Both                 |
| `clear_context()`              | Method  | ✅         | Clears the context dictionary                    | Both                 |
| `clear_to_email()`             | Method  | ✅         | Clears the recipient(s)                          | Both                 |
| `clear_from_email()`           | Method  | ✅         | Clears the from address                          | Both                 |
| `clear_html_template()`        | Method  | ✅         | Clears the HTML template                         | Both                 |
| `clear_text_template()`        | Method  | ✅         | Clears the text template                         | Both                 |
| `clear_all_fields()`           | Method  | ✅         | Clears all email-related fields                  | Both                 |

#### **Database Access**

| Name                           | Type    | Chainable | Description                                      | Defined In           |
|---------------------------------|---------|-----------|--------------------------------------------------|----------------------|
| `add_email_sender_instance()`  | Method  | ✅         | Inject an EmailSender into the logger wrapper    | `EmailSenderLogger`  |
| `add_log_model()`              | Method  | ✅         | Attach a model to persist email logs             | `EmailSenderLogger`  |
| `enable_email_meta_data_save()`| Method  | ✅         | Enables saving of email meta to the database     | `EmailSenderLogger`  |

#### **Logging and Verbose Functions**

| Name                           | Type    | Chainable | Description                                      | Defined In           |
|---------------------------------|---------|-----------|--------------------------------------------------|----------------------|
| `log_only_fields()`            | Method  | ✅         | Only log specific fields                         | `EmailSenderLogger`  |
| `exclude_fields_from_logging()`| Method  | ✅         | Exclude fields from logging                      | `EmailSenderLogger`  |
| `start_logging_session()`      | Method  | ✅         | Enable logging mode                              | `EmailSenderLogger`  |
| `stop_logging_session()`       | Method  | ✅         | Stop logging and finalise log object             | `EmailSenderLogger`  |
| `pause_logging()`              | Method  | ✅         | Temporarily stop logging changes                 | `EmailSenderLogger`  |
| `resume_logging()`             | Method  | ✅         | Resume logging after a pause                     | `EmailSenderLogger`  |
| `enable_verbose()`             | Method  | ✅         | Enable verbose logging                           | `EmailSenderLogger`  |
| `disable_verbose()`            | Method  | ✅         | Disable verbose logging                          | `EmailSenderLogger`  |
| `set_custom_formatter()`       | Method  | ✅         | Set a formatter for custom log formatting        | `EmailSenderLogger`  |
| `set_traceback()`              | Method  | ✅         | Enable stack trace logging on errors and the order methods were called           | `EmailSenderLogger`  |
| `config_logger()`           | Method  | ✅         | Configure logger object and the log level            | `EmailSenderLogger`  |



#### **Logging Level Methods**

| Name                           | Type    | Chainable | Description                                      | Defined In           |
|---------------------------------|---------|-----------|--------------------------------------------------|----------------------|
| `to_info()`                    | Method  | ✅         | Changes the level to info                         | `EmailSenderLogger`  |
| `to_debug()`                   | Method  | ✅         | Changes the level to debug                        | `EmailSenderLogger`  |
| `to_warning()`                 | Method  | ✅         | Changes the level to warning                      | `EmailSenderLogger`  |
| `to_error()`                   | Method  | ✅         | Changes the level to error                        | `EmailSenderLogger`  |

   
#### **Properties and Metadata**

| Name                           | Type      | Chainable | Description                                      | Defined In           |
|---------------------------------|-----------|-----------|--------------------------------------------------|----------------------|
| `is_email_sent`                | Property  | ❌         | Property that returns if the email was sent      | `EmailSenderLogger`  |
| `email_delivery_count`         | Property  | ❌         | Property that returns number of deliveries       | `EmailSenderLogger`  |
| `email_meta_data`              | Property  | ❌         | Returns metadata of sent email                   | `EmailSenderLogger`  |
| `payload`                      | Property  | ❌         | Property returning the full internal state       | `EmailSenderLogger`  |
| `return_successful_payload()`  | Method  | ❌         | Returns a copy of the payload (audit fields)     | `EmailSenderLogger`  |

---

### **Explanation of Categories:**

- **Core Functions**: The main email sending functionality, like setting recipients, subject, context, templates, headers, and clearing fields.
  
- **Database Access**: Methods that deal with interacting with a database, logging email details, saving email meta data, and configuring the logger.
  
- **Logging and Verbose Functions**: Methods that manage the logging session, verbosity, and custom log formatting.

- **Properties and Metadata**: Methods that return properties related to the email state, including whether it was sent, the delivery count, and email metadata.


---
[🔝 Back to top](#table-of-contents)


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


django-email-sender is a Django package that allows you to send emails using customizable templates, with easy-to-use methods for setting the sender, recipients, subject, and context.

## Installation

To install the package:
```pip install django-email-sender ```


For more details, visit [the PyPI page](https://pypi.org/project/django-email-sender/).

[🔝 Back to top](#table-of-contents)


## Requirements

- **Python 3.10+**  
  This library uses [Structural Pattern Matching](https://docs.python.org/3/whatsnew/3.10.html#structural-pattern-matching), introduced in Python 3.10, via the `match`-`case` syntax.

### Why Python 3.10?

One of the key features used in this project is the `match`-`case` syntax, which offers a more readable and expressive way to handle complex conditional logic.

#### Example Usage:

```python
def log_level_handler(level: str) -> str:
    match level.lower():
        case "debug":
            return "Logging in debug mode"
        case "info":
            return "Standard info logging"
        case "warning":
            return "Warning: Check your configuration"
        case "error":
            return "Error occurred during processing"
        case _:
            return "Unknown logging level"
```
This syntax is not available in versions prior to Python 3.10, so attempting to run the library on an earlier version will raise a `SyntaxError`.


- Dependencies:  
  List of required dependencies (install with `pip install -r requirements.txt`)

## Compatibility

This package has been tested against Django 5.2 (the latest version at the time of release) and is known to work with versions 3.2 and above.

⚠️ **Compatibility with Django 6.x and beyond is not yet guaranteed.** If you're using a future version, proceed with caution and consider opening an issue if anything breaks.


[🔝 Back to top](#table-of-contents)

---

### Logger and Database Integration

🧩 `EmailSender`via `EmailSenderLogger`, supports optional integration with both logging and database persistence for email sending events.

### Logging Integration

🪵 `EmailSenderLogger` does not provide a built-in logger. You must configure and pass your own logger (e.g., using Python’s built-in logging module). If no logger is provided, EmailSenderLogger will still function as expected — silently and without log output.

`Key Points`:
> If you pass a logger, it will be used as-is.

> EmailSenderLogger does not modify logger levels, handlers, or formatters.

> If you do not set a logger level (e.g., INFO, DEBUG), the logger will be ignored.

> If no logger is configured, email sending proceeds normally, without logging.
> If you do not configure your formatting then default spacing will be used which may or may not align depending if you are using different levels


### `config_logger`

The `config_logger` method is entirely optional. You only need to call it if you want to enable logging for `EmailSenderLogger`. If not called, `EmailSenderLogger` will skip all logging operations and focus solely on sending the email — no setup required, no extra overhead.

To enable logging, you must also call:

- **`start_logging_session()`**  
   This ensures that logging starts. Without calling this, the logger will not log anything.

This setup gives you full flexibility:

- Enable logging when you need visibility into the email-sending process.
- Skip logging for quicker or simpler email sends.
- `EmailSender` adapts to your needs — whether you prefer a fully monitored pipeline or a fast, lightweight send.


###  How to configure the Logger 

🔗 Once the user has configured a logger, it can be passed using the `config_logger` chain method.  
Use `LoggerType` to minimise errors and ensure consistency across your implementation.  
See [Logger Configuration](#logger-configuration) for a full list of supported types and usage examples.

The parameters available for `config_logger` are:

| Parameter    | Type                        | Description                                         |
| ------------ | --------------------------- | --------------------------------------------------- |
| `logger`     | `Logger` instance (required) | The logger instance provided by the user.           |
| `log_level`  | `LoggerType` str (required) | The log level to listen to (e.g., "info", "error"). |


### 📝 Notes

  - If no logger is set, `EmailSenderLogger` will **not log anything**

     - **Advanced users** may customise logging heavily using the `custom_formatter`.
     - **Casual users** can simply provide a logger and rely on default behaviour.
     - **Users not interested in logging** can simply skip the set logger setup and proceed with sending emails.

---

## Example Setting up a simple Logger with EmailSenderLogger

In this section, we'll configure a Python simple logger and demonstrate how to integrate it with `EmailSenderLogger`.

```python

import logging
from django_email_sender.email_sender import EmailSender
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.email_sender_constants import LoggerType

# Step 1: Set up a basic logger
logger = logging.getLogger("email_sender_logger")

# Optional: Add a console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(console_handler)

# Step 2: (Optional) Define a custom formatter
def my_custom_formatter(exception: Exception, trace: str) -> str:
    return f"Error occurred: {str(exception)} | Traceback: {trace}"

# Step 3: Use the logger with EmailSender

  email_sender = (
      
      EmailSenderLogger.create().start_logging_session()
    
         .enable_verbose()
         .config_logger(logger, LoggerType.DEBUG) # logger added
         .add_email_sender_instance(EmailSender.create())
         .from_address("no-reply@example.com")
         .to("no-reply@example.com")
         .with_subject("test subject")
         .with_html_template("test_email.html")
         .with_text_template("test_email.txt")
         .send()
    
)

```

### 📋 Whats Exactly Is Happening Here?

| Step | What |
| :-- | :-- |
| **1** | We create a simple logger using Python’s built-in `logging` module. |
| **2** | (Optional) We define a `custom_formatter` for formatting error messages. |
| **3** | We chain `set_logger()` with other `EmailSender` methods like `to(...)`, `with_subject(...)`, `with_context(...)`, and finally `send()`. |


---

[🔝 Back to top](#table-of-contents)


## Reuse the Logger and Formatter Across Multiple Emails

If you have set up a custom logger or formatter setup and plan to send multiple emails, **you don't need to set them up every single time**.

Instead, you can **set them once** when you create an instance of `EmailSenderLogger`, then **reuse the same instance** to send all your emails.  

This way:
- Your logger and formatter stay attached to the instance.
- You avoid repetitive setup code.
- Sending emails becomes much cleaner and faster.

---

### Resetting or Reusing the Instance Cleanly

When reusing the same `EmailSender` or `EmailSenderLogger` instance to send multiple emails, certain fields (like recipients, subject, or context) may retain values from previous emails, especially if you're not overriding them. Since you're using a single instance of `EmailSender` or `EmailSenderLogger` if you are interested in logging or storing the data in a database then no errors will occur when calling the `send` method again, as these fields were set to required values earlier.

However, this can lead to issues where you might unintentionally send emails with the wrong template, subject, or even to the wrong recipient.

To avoid this, you have two options:

1. **Use the `auto_reset` flag**: Set it to `True` to clear all fields before sending the next email.
2. **Manually clear specific fields**: Call the appropriate `clear_<field_name>` method (e.g., `clear_subject()`, `clear_context()`, `clear_all_fields()`, etc.) to reset only the fields you need.


### 🚀 Example Usage 
#### The example focuses on using the `auto_reset` flag to clear the fields but this can be done using the corresponding clear_<field_name> method

```python
# Step 1: Create an instance and set the logger/formatter once
email_sender = EmailSenderLogger.create().config_logger(
    logger=logger,
    log_level=LoggerType.ERROR,
)

# Step 2: Send multiple emails using the same instance

# Example 1 - Send email 1
(
    email_sender.from_address("no-reply@example.com")
        .to(["test@example.com"])
        .with_subject("Verify Your Email")
        .with_context({"username": "John", "verification_code": "123456"})
        .with_html_template("verification.html", folder_name="verification")
        .with_text_template("verification.txt", folder_name="verification")
        .send(auto_reset=True)  # ensure a clean state
)

# Example 2 - Send email 2
# auto_reset is not set to true, default of False is used
(
    email_sender.from_address("no-reply@example.com")
        .to(["test@example.com"])
        .with_subject("Welcome Email")
        .with_html_template("welcome.html", folder_name="welcome")
        .with_text_template("welcome.txt", folder_name="welcome")
        .send()
)

# Example 3 - Send email 3
# Since `auto_reset` wasn't set in Example 2, and the user is not overriding the fields, the `welcome.html` and `welcome.txt` templates 
# will be used for the third email, even though the subject ("Import Account Information") doesn't match the templates.
# This mismatch will result in the recipient receiving an email with irrelevant content.
# To avoid this issue, you should either manually clear the fields or use `auto_reset=True` to ensure a clean state.
(
    email_sender.from_address("no-reply@example.com")
        .to(["test@example.com"])
        .with_subject("Meetup Information time and location")
        .send(auto_reset=True)  # ensure a clean state
)

```

✅ **All emails are sent using the same instance, with the logger and formatter already set up.**

### Tip

> If you are sending dozens of emails with the same logger and configuration, reusing `.clear_all_fields()` might save you tiny performance overhead.
But if you're only sending 1–2 emails each time, it's easier to just create a fresh instance!


---

### ✨ Why This Matters

- **Performance**: Avoids re-initialising the logger every time.
- **Cleaner Code**: Reduces duplication and clutter.
- **Consistency**: Ensures all emails follow the same logging/formatting rules.

---

### ✨ Key Points:

  - **By default** : EmailSenderLogger doesn't log events to the console or file unless an error occurs
  - **Custom logger**: Use the `config_logger` method if you need more control over logging, like logging to a file or an external service, See the flow of the email process, sending, delivery, errors, etc
  - **Logging configuration**: You can configure your logger with handlers, formats, and levels as needed via the `settings.py`
  which can be overriden when using `EmailSenderLogger`

✅ Easy for beginners  
✅ Powerful for advanced users

---

[🔝 Back to top](#table-of-contents)

###  Tracing Method Chains and logging errors with `set_traceback`

🧭 If you ever wanted to know exactly which methods were called during your email building process, `set_traceback()` is your friend. It provides a step-by-step breakdown of the chained method calls that lead up to sending an email.

#### This is especially useful for debugging complex chains, understanding the flow, or simply verifying that everything is working in the expected order. 

### Why Use Method Tracing?

When working with complex chains of method calls or deeply nested logic, it can be difficult to understand the exact flow of execution. Method tracing provides a powerful way to gain visibility into what's happening under the hood.

- **Debug complex chains** with greater ease  
- **Understand execution flow** step-by-step  
- **Verify correct method ordering and dependencies**

### Enabling chain tracing

> To enable method tracing, you must:
> - Set `method_tracing ` parameter in the `set_traceback` method to `True`
> - Call `enable_verbose()`
> - set the level to `Debug` either by the `config_logger` or using the `.to_debug()` method

Chain tracing is only shown at the `debug level` and when `enable_verbose` mode is enabled to avoid overwhelming the user with too much information.

### Here's how it works:

1. **Method Chain Tracking**  
   The method chain begins from the initial call (e.g., `create()`) and continues through all chained methods like `to()`, `with_subject()`, and so on. Each method gets logged in real-time.

### ⚙️ Behind the Scenes (Optional Detail for Power Users)

Internally, `show_traceback()` appends each method name and its arguments to a trace log as the chain is built. This is particularly helpful in:

- Debugging method order issues
- Catching repeated or conflicting method calls
- Understanding flow when extending or contributing to the library


### 🧪 Example Output from `set_traceback(method_tracing=True)`

When `set_traceback(method_tracing=True)` is enabled, you’ll see something like this in your logs or console (depending on your logger configuration):

```

\[TRACE] Method Chain Started:
→ create()
→ start\_logging\_session()
→ config\_logger()
→ add\_email\_sender\_instance()
→ from\_address()
→ to()
→ with\_subject()
→ with\_text\_template()
→ send()

````

Each arrow (`→`) represents a method call in your builder chain. This gives you full visibility into what’s been run before `.send()` is triggered.

---

2. **Verbose Debugging**  
   If `show_traceback=True` is enabled, **stack trace information is included** in the logs when an error happens. This includes:
   - The sequence of method calls leading to the error.
   - Detailed information about the error (e.g., the specific line number, method name, and error message).
   
   This allows you to track back to the root cause of an issue quickly and effectively.

### Example of an error traceback:

Consider an email sending process like this:

```python

# Assume the neccessary modules have been imported

email = EmailSenderLogger.create() \
       .start_logging_session()\
        .enable_verbose()\
        .add_email_sender_instance(EmailSender())\
        .config_logger(logger, LoggerType.DEBUG)\
        .set_traceback(method_tracing=True, show_traceback=True)\
        .to("recipient@example.com") \
        .with_subject("Test Email") \
        .with_html_template("invalid_test_template.html") \

    .... other methods here
    .send()
```

Now, let’s assume that there’s an error while sending due to an invalid template, and you've set `show_traceback=True`. The logged traceback might look like this:

```
[DEBUG][METHOD_TRACE] Method Chain Started: EmailSenderLogger._get_environment() → EmailSenderLogger._create_meta_data() → EmailSenderLogger._validate_template() → EmailSenderLogger._send()
--- Error Traceback ---
File "email_sender.py", line 145, in _send
    raise TemplateNotFoundError("HTML template not found")
TemplateNotFoundError: HTML template not found
```

### Breakdown of what happens:

* The log shows the exact method calls that were made in the process.
* The error is flagged, and the traceback reveals where the failure occurred— in the `_send()` method, specifically due to a `TemplateNotFoundError`.
* You can now see **exactly** which method caused the problem and what the error was, making it easier to debug.

### Why is this useful?

* **Debugging Complex Chains**: If you're chaining many methods together, it’s often hard to track down where an error happens. `show_traceback=True` ensures that you know exactly where to look.

* **Detailed Logging**: You get more than just a "method failed" message; you get a full traceback that includes method names, file locations, and specific error messages, which can greatly speed up debugging.


You can also do something like this to ensure that you always have a traceback

```python

# Assume the necessary modules have been imported
import os

email_sender = (
    EmailSenderLogger.create()
        .start_logging_session()
        .config_logger(logger)
        .add_email_sender_instance(EmailSender)
        .from_address("dev@example.com")
        .to("debug@example.com")
        .with_subject("Dev Mode Email")
        .with_text_template("dev_template.txt", "emails")
)

# Automatically enable tracing in dev
if os.getenv("ENV") == "development":
    email_sender.set_traceback(True, True)
    email_sender.enable_verbose()

email_sender.send()

```
[🔝 Back to top](#table-of-contents)


## Turning on Verbose Mode

When using `EmailSenderLogger`, depending on the log level you’ve chosen (`info`, `warning`, `error`, or `debug`), you'll see information corresponding to those levels. By default, the logger doesn't show detailed step-by-step information to avoid overwhelming you. Instead, it focuses on providing the most relevant details for debugging.

However, if you want to view more detailed information, you can enable verbose logging with the `enable_verbose()` method. When enabled, you’ll see extra details that would normally be hidden. Note that `enable_verbose` will show the additional information based on the log level you’ve selected. For example:

- In `debug` mode, you'll see logs from all levels: `debug`, `info`, `warning`, and `error`.
- In `info` mode, you'll see `info`, `warning`, and `error` logs.
- In `warning` mode, you'll see `warning` and `error` logs.
- In `error` mode, you'll only see `error` logs.

To use verbose logging, simply chain the `enable_verbose()` method. To disable verbose mode, use the `disable_verbose()` method.

Example usage:

```python

# assume that neccessary modules have been imported

email_sender = (
    EmailSenderLogger.create()
    .start_logging_session()
    .config_logger(logger, LoggerType.INFO)
    .enable_verbose()  # Enable verbose mode
    .add_email_sender_instance(EmailSender)
    .from_address("test@example.com")
    .to("recipient@example.com")
    .send()
)

```
---
[🔝 Back to top](#table-of-contents)


## Setting up an advanced logger

In the above example we set up a very limited logger that doesn't involve the user configure the `settings.py` file, however that 
logger has several limited.

⚠️ Limitations:

- **Logger might duplicate messages:**
  - Django automatically configures logging early during startup, which may cause the logger to propagate messages up to Django’s root logger.
  - This could result in messages being printed twice: once by your `console_handler` and once by Django’s default logger.

- **No control through Django settings:**
  - You can't easily change logging behaviour (e.g., send email errors, write to file, silence logs in production) through Django’s `LOGGING` configuration if you manually build loggers everywhere.

- **Handler added multiple times:**
  - If the code runs multiple times (e.g., Django imports modules multiple times), you could end up attaching multiple handlers, which causes duplicate log messages.

### To configure your email_sender_logger properly through Django's LOGGING settings

EmailSender via EmailSenderLogger supports flexible logging integration.
To enable logging, configure a logger in your Django settings.py (or your project settings) like this:

```python

# -------------------------------------------------------------------
# settings.py
#--------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # required so Django's default logging still works
    "formatters": {
        'right_indented': {
            '()': 'your-app-path-to-this-file.RightIndentedFormatter',  # Update with the correct path to your custom formatter
            'format': '[%(asctime)s] %(levelname)-8s %(name)-13s: [%(message)s]',
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "right_indented",  # Use 'right_indented' formatter here
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "emails.log",  # Specify your log file name here
            "formatter": "right_indented",  # Use 'right_indented' formatter here
        },
    },
    "loggers": {
        "email_sender": {  # Logger name used by EmailSender or whatever name you chose
            "handlers": ["console", "file"],  # Both handlers for console and file
            "level": "DEBUG",  # Set log level to DEBUG or as needed
            "propagate": False,  # This prevents propagation to parent loggers
        },
    },
}

```

Now create a `utils.py` file (or choose a name that suits your project) inside your app folder, and define your custom formatter there. This ensures proper indentation and structure for logging output, as shown below.

```plaintext


[2025-05-08 06:49:56,087] INFO     email_sender : Some information
[2025-05-08 06:49:56,087] DEBUG    email_sender : Some Debug message
[2025-05-08 06:49:56,195] WARNING  email_sender : Some Waringin
[2025-05-08 06:49:56,195] Error    email_sender : Some Waringin
```

```python

# -------------------------------------------------------------------
# utils.py  
#--------------------------------------------------------------------
import logging

class RightIndentedFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        
        # Add a custom indent to the beginning of the log message
        original_message = super().format(record)
        return f"    {original_message}"  # 4 spaces or any amout of space you want

```
Note:
  Make sure to link `formatter` file in the `LOGGER` with the `settings.py` and now whenever
  you send an email it will nicely be displayed in a formatted setting.


## Advanced Tip: Rotate Log Files Automatically

For larger applications, it's recommended to rotate your log files to avoid growing indefinitely.
You can modify the file handler to automatically create a new log file each day:

```python
from logging.handlers import TimedRotatingFileHandler

"handlers": {
    "file": {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": "django.log",
        "when": "midnight",  # Create a new file every midnight
        "backupCount": 7,    # Keep last 7 days of logs
        "formatter": "standard",
    },
},
```
This will keep your logs clean without manually deleting old files.

[🔝 Back to top](#table-of-contents)


## Advanced Logger Usage

`EmailSenderLogger` allows you to monitor and capture detailed information while using the `EmailSender`. You can configure it in various ways depending on how much control or verbosity you need.

The most straightforward usage is to configure the logger with a specific log level — such as `ERROR`, `WARNING`, `INFO`, or `DEBUG` — and let it automatically log events to the console or a file.

---

## 🔹 First Approach
### Set up the Logger with a Log Level

You can initialise a logger and attach it to `EmailSenderLogger` to record activity at a chosen level. This is useful for capturing general usage, errors, or debugging info.

```
```python

EmailSenderLogger.create().config_logger(
    logger=logger, 
    log_level=LoggerType.ERROR
)

```

### Second Approach

###  .log_only_fields(*fields)
Use the .log_only_fields() method to log only specific fields you're interested in.

This gives you fine-grained control and avoids cluttering your logs with unnecessary data.
To use this method, import `EmailSenderConstants` and pass in the fields you'd like to track.
See the full list of fields under [`EmailSenderConstants`](#emailsenderconstants).

```python
from django_email_sender.constants import EmailSenderConstants

EmailSenderLogger.create()
    .start_logging_session()
    .config_logger(logger, LoggerType.DEBUG) # start of debug
    .log_only_fields(
        EmailSenderConstants.Fields.SUBJECT.value,
        EmailSenderConstants.Fields.TO_EMAIL.value
    )

```

---

## 🔹 Third Approach
### `.exclude_fields_from_logging(*fields)`

Sometimes, you might want to log *everything except* certain fields.  
The `.exclude_fields_from_logging()` method allows you to omit specific fields from being recorded in your logs.

This is especially useful when logging sensitive data such as emails or templates, or just to reduce noise.

```python
from django_email_sender.constants import EmailSenderConstants

EmailSenderLogger.create()
    .start_logging_session()
    .config_logger(logger, LoggerType.DEBUG) # start of debug
    .exclude_fields_from_logging(
        EmailSenderConstants.Fields.HTML_TEMPLATE.value,
        EmailSenderConstants.Fields.CONTEXT.value
    )
```

> ⚠️ **Note:** Do not use `.log_only_fields()` and `.exclude_fields_from_logging()` together.
> These methods are mutually exclusive—use one or the other depending on your logging preference.



### 🔄 Change Levels Dynamically During Logging
During the logging process, you may wish to change levels to capture different aspects of what’s happening. For instance, you might start in `DEBUG` mode and then switch to `INFO`, `WARNING`, or `ERROR` depending on what data you want to capture.

You can do this using `.to_debug()`, `.to_info()`, `.to_warning()`, and `.to_error()` — all without restarting or reconfiguring the logger.

````python


#### 🧪 Example 1 – Switching Levels While Chaining
```python

# Assume Logger and EmailSender have been imported and linked

email_sender = (
    EmailSenderLogger.create().start_logging_session()
        .config_logger(logger, LoggerType.DEBUG)       # Start at DEBUG
        .add_email_sender_instance(EmailSender)
        .from_address("test@example.com")
        .to_info()                                     # Switch to INFO
        .to("jackie@example.com")
        .to_warning()                                  # Switch to WARNING
        .with_subject("test subject")
        .with_html_template("test_email.html", "sender")
        .with_text_template("test_email.txt", "sender")
        .to_error()                                    # Final switch to ERROR
        .send()
)
````

#### 🧪 Example 2 – Changing Levels with `config_logger`

You can also switch levels inline by re-calling `.config_logger()`.

```python
from django_email_sender.email_sender import EmailSender, LoggerType
import logging

logger = logging.getLogger("email_sender")

(
    EmailSenderLogger.create()
        .config_logger(logger, LoggerType.DEBUG)
        .from_address("no-reply@example.com")
        .to(["jtest@example.com"])
        .config_logger(logger, LoggerType.INFO)
        .with_subject("test")
        .config_logger(logger, LoggerType.WARNING)
        .with_context({"username": "John", "code": "123456"})
        .with_headers({"X_HEADER": "some header"})
        .config_logger(logger, LoggerType.ERROR)
        .with_html_template("test_email.html", folder_name="sender")
        .with_text_template("test_email.txt", folder_name="sender")
        .send()
)
```

---

###  Cancel or Pause Logging Mid-Flow

🛑 If you only want to log certain parts of your flow, you can stop or pause the logger at any point.

Use the following methods:

 [`start_logging_session()`](#start-logging-session) — starts the logging session.
- [`stop_logging_session()`](#stop-logging-session) — permanently stops logging for the current flow.
- [`pause_logging()`](#pause-logging) — temporarily halts logging.
- [`resume_logging()`](#resume-logging) — resumes logging after a pause.

#### Example: Stopping the Logging Session

```python
# Assume Logger and EmailSender have been imported and linked

email_sender = (
    EmailSenderLogger.create().start_logging_session()
        .config_logger(logger, LoggerType.DEBUG)
        .add_email_sender_instance(EmailSender)
        .from_address("test@example.com")
        .to("jackie@example.com")
        .stop_logging_session()  # Logging ends here
        .with_subject("test subject")
        .with_html_template("test_email.html", "sender")
        .with_text_template("test_email.txt", "sender")
        .send()
)
```

Anything after the `.to()` field will not be captured in the logs.

#### Example: Pausing and Resuming Logging

```python
email_sender = (
    EmailSenderLogger.create().start_logging_session()
        .config_logger(logger, LoggerType.DEBUG)
        .add_email_sender_instance(EmailSender)
        .from_address("test@example.com")
        .to("jackie@example.com")
        .pause_logging()                     # Temporarily pause
        .with_subject("test subject")        # Not logged
        .resume_logging()                    # Logging resumes
        .with_html_template("test_email.html", "sender")
        .with_text_template("test_email.txt", "sender")
        .send()
)
```

---

Key points
    - Provides advanced way to log or monitor or your data
    - Allows you set log points between two methods e.g two fields
    - Allows you to an `end point` where it can then run up to
    - Does force you to use these advanced featues, you can just as easily set up with `config_logger` and let run or use no logger at all
    - It is easier for beginners to use and allows `advanced` users and more control to advanced user

[🔝 Back to top](#table-of-contents)


## Database Integration

`EmailSenderLogger` allows users to optionally persist email metadata to a database. This is useful for audit logs, diagnostics, and history tracking.

🔔 Note: `EmailSenderLogger` does not create or manage any database tables. You must define your own log model, and explicitly opt in to database logging.

`Requirements`:

> You must create your own model that inherits from EmailBaseLog.

> The model must be passed as a class, not an instance, using .add_log_model().

> You must explicitly enable database logging using .enable_email_meta_data_save().

> If no valid model is added, no data will be saved



### 📄 Example: Custom Email Log Model

```python

# models.py

from django_email_sender.models import EmailBaseLog 

class CustomEmailLog(EmailBaseLog):
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

### 🛠️ Usage in Code

```python

from django_email_sender.email_sender import EmailSender
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

---
[🔝 Back to top](#table-of-contents)

---
## 🔍 Payload & Metadata Access

### Payload Inspection

`EmailSenderLogger` provides structured access to the **full email payload** in json via the `.payload` property. 

This enables developers to **inspect**, **log**, or **persist** detailed data related to any email being sent. The payload is **dynamically constructed**, allowing you to access and inspect it either **after sending the email** or **as you build each field** during the setup process.


### ✅ What the Payload Includes:
- `from_email` → Email address of the sender  
- `to_email` → List or string of recipient addresses  
- `subject` → Subject line of the email  
- `body_html` → HTML version of the message  
- `body_text` → Plain-text version of the message  
- `context` → Context dictionary used to render the template  
- `headers` → Any custom headers attached to the message  

### ⚠️ Why This Method Is Not Chainable

Unlike other methods in `EmailSender`, this one is **not chainable**. This is intentional.

The purpose of the method is to return a structured payload containing dynamic email data such as `from_email`, `to_email`, `subject`, `body_html`, etc. Since `EmailSenderLogger` assumes you may need to **inspect, log, or persist** this data, the method returns the payload directly instead of returning the instance (`self`).

This design ensures developers have **immediate access** to the email data when they need it — whether during construction or after sending to either inspect or use as part of the application. Making it chainable would require additional steps to extract the data, which would reduce clarity and usability.


### 📦 Example usage :
```python
payload = email_sender.payload
print(payload)
# {
#   "from_email": "admin@example.com",
#   "to_email": ["user@example.com"],
#   "subject": "Welcome to Our Platform",
#   "body_html": "<h1>Welcome!</h1>",
#   "body_text": "Welcome!",
#   "context": {"username": "john_doe"},
#   "headers": {"X-Custom-Header": "value"}


or 

# use the data somewhere in your application

```
[🔝 Back to top](#table-of-contents)


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

```python
from django_email_sender.email_sender import EmailSender

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
│       ├── welcome_email.html
│       └── welcome_email.txt


```

#### Custom Setup (with `MYAPP_TEMPLATES_DIR` defined):
```
my_project/
│
├── custom_templates/
│   └── emails_templates/
│       ├── welcome_email.html
│       └── welcome_email.txt

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

This guide shows how to use `django-email-sender` in a Django project to send a verification email. This will not be using a logger. [See the logger section](#logger) See logger section on how to use `EmailSender` with a logger.

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


### Playing Around with Features Without Sending Emails

🧪 You can quickly test various features of `EmailSenderLogger` by setting up a simple view. Here's how:

1. **Set up a sample view** in your Django app.
2. Add this to your `settings.py` to log emails to the console:

   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```
3. Add **`<a-html-template>.html`** and **`<a-test-template>.txt`** templates to your `templates` directory to avoid template errors.

   * **`html template`**: Your basic HTML structure.
   * **`text template`**: Your basic text structure.
4. Now, all emails sent will be logged in the **console** only, without actually sending to real email addresses.
5. You can safely test features like:

   * **Logging**: Track the email sending process and potential errors.
   * **Field Filtering**: Choose which fields to log or save, such as subject, from email, or the context.
   * **Metadata Storage**: Save email metadata (like recipients, subject, timestamp) to a database for auditing purposes.
6. View the logging output in your console or test out these features.

#### What is `django.core.mail.backends.console.EmailBackend`?

It **replicates** the entire process of sending an email but logs it to the console instead of actually sending it to an address. This allows you to test the email-related features of `EmailSenderLogger` safely without sending real emails.

### Example View

```python
# views.py

import logging
from django.http import HttpResponse
from your_app.models import CustomEmailLog
from django_email_sender.email_sender import EmailSender
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.email_sender_constants import LoggerType, EmailSenderConstants

# Assume logger is configured in settings.py
logger = logging.getLogger("email_sender")

def test_email(request):
    email_sender_logger = EmailSenderLogger.create()
    (
        email_sender_logger
        .start_logging_session()
        .enable_verbose()
        .add_email_sender_instance(EmailSender())
        .add_log_model(CustomEmailLog)
        .enable_email_meta_data_save()
        .config_logger(logger, LoggerType.DEBUG)
        .log_only_fields(
            EmailSenderConstants.Fields.CONTEXT.value,
            EmailSenderConstants.Fields.SUBJECT.value,
            EmailSenderConstants.Fields.FROM_EMAIL.value,
            EmailSenderConstants.Fields.TEXT_TEMPLATE.value,
        )
        .reset_field_logging_filters()
        .from_address("no-reply@gmail.com")
        .to("to-reply@gmail.com")
        .with_subject("Subject Line")
        .with_html_template("test_email.html", "sender")
        .with_text_template("test_email.txt", "sender")
        .send()
    )

    print(email_sender_logger.payload)
    print(email_sender_logger.email_meta_data)
    print(email_sender_logger.return_successful_payload())

    return HttpResponse("Email sent successfully!")
```
---

**Key Points:**

* **Test out features** by logging email data to the console instead of sending actual emails.
* This process allows you to safely check the logging, field filtering, metadata, payload, emails database storage features, etc without worrying about sending real emails to recipients.


[🔝 Back to top](#table-of-contents)


## Best Practices

### 1. **Configure a Logger in Production**
   - Always configure a logger for production environments to track errors and activities.
   - Ensure that your logger is properly set up before calling `.send()`. This helps with debugging and provides valuable insights into any email issues.

### 2. **Use `.send()` as the Final Call**
   - The `.send()` method should be the last call in your chain. Ensure all other configurations (like `to()`, `from_address()`, etc.) are set before calling `.send()`.

### 3. **Logging Customization**
   - For more advanced logging, customize the format by providing a `custom_formatter` function. This can help format error messages or traceback details according to your needs.
   - The `custom_formatter` function must accept two arguments: an `Exception` and a `traceback` string. This ensures security and prevents injection vulnerabilities.

### 4. **Set Traceback Visibility During Development**
   - Set the `show_traceback=True` flag during development to view detailed error traces. This is helpful for debugging, but should be turned off in production to avoid exposing sensitive information.

### 5. **Related folder names**

- **Use the same `folder_name` for related templates (text and HTML):**  
  This keeps your project **organised**, **consistent**, and **easy to maintain**.

    ```plaintext
    project/
    ├── templates/
    │   └── email_templates/
    │       └── authentication/
    │           ├── login/
    │           │   ├── login.html
    │           │   └── login.txt
    │           ├── passwords/
    │           │   ├── password_reset.html
    │           │   └── password_reset.txt
    │           └── register/
    │               ├── register.html
    │               └── register.txt

---
[🔝 Back to top](#table-of-contents)


## Worst Practices


### 1. **Skipping Logger Configuration**
   - **Avoid skipping logger configuration**, especially in production. Not configuring a logger will result in missed error details, making it much harder to debug issues. Always pass a logger if you want insights into what's happening during the email sending process.

### 2. **Calling `.send()` Before Finalizing Email Details**
   - **Don’t call `.send()` before setting all required email details** like `to(...)`, `from_address(...)`, `with_subject(...)`, etc. Calling `.send()` will result in an error raised.

### 3. **Using a Custom Formatter with Incorrect Parameters**
   - **Don’t pass an invalid custom formatter**. The `custom_formatter` function must accept exactly two arguments: an `Exception` and a `traceback` string. Passing in incorrect arguments will result in an error being raised.

### 4. **Leaving Tracebacks Visible in Production**
   - **Never leave detailed tracebacks visible in production**. Tracebacks should only be shown in a development environment. Exposing them in production can reveal sensitive information to users or attackers, potentially causing security issues.

### 5. **Ignoring Error Handling for Email Failures**
   - **Don’t ignore errors** when email sending fails. Always ensure you have error handling in place, whether it’s logging or retries, so that you’re aware of any issues that occur during the email process.

### 6. **Mixing Different Log Levels without Thought**
   - **Don’t randomly mix log levels** without a clear purpose. Choose a log level for each message carefully (`INFO`, `WARNING`, `ERROR`, etc.) to make your logs structured and easy to interpret.
### 7. **Skipping the logger** 
 - Skipping the logger and then struggling to debug when an email fails.

### 5. **Mixing unrelated templates together randomly:**
- **Keeping related files in a different `folder_name`** 
For example :  
This makes your project **messy**, **error-prone**, and **hard to maintain**.
  


    ```plaintext
    project/
    ├── templates/
    │   └── email_templates/
    │       ├── login.html
    │       ├── password_reset.txt
    │       ├── newsletter.html
    │       ├── random_folder/
    │           ├── register.txt
    │       ├── backup_templates/
    │           ├── login_backup.txt
    │           └── reset_password_backup.html
    │       └── marketing/
    │           ├── new_product.html
    │           └── welcome.txt
    ```

- **Key issues:**  
  - Templates from different features (login, passwords, marketing) are **thrown together** with no clear separation.
  - Some templates are **floating randomly** without folders.
  - Backup files are mixed with production files.
  - Inconsistent folder naming (`random_folder`, `backup_templates`, etc).
  - Future developers (even you!) will **struggle** to find the correct template.
  - Higher chance of using the wrong template by mistake.


---
[🔝 Back to top](#table-of-contents)



## License
 - This package is licensed under the MIT License. See the LICENSE file for details.

## Credits
 -This library was created and maintained by Egbie Uku a.k.a EgbieAndersonUku1.

[🔝 Back to top](#table-of-contents)

