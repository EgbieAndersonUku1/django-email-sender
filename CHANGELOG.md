# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-05-11

### Public API

- **Database Logging Support (Optional)**
  - Users can now integrate database-backed logging for sent emails or errors.
  - Completely decoupled; pluggable via dependency injection. No built-in model is enforced.

- **Custom Exception Formatter (Optional)**
  - Accepts a user-defined function for formatting exceptions before logging.
  - Must be callable, accept one or two arguments (`Exception`, optional `traceback`), and return a string.
  - Automatically validated on assignment.

**Clear Methods for Reusability**
  - `.clear_all_fields()` — Resets all fields (subject, recipient emails, body templates) to ensure a clean state.
  - `.clear_context()` — Clears any stored context for the email.
  - `.clear_from_email()` — Clears the sender's email address.
  - `.clear_to_email()` — Clears the recipient's email addresses.
  - `.clear_subject()` — Resets the email subject.
  - `.clear_html_template()` — Clears the HTML template content.
  - `.clear_text_template()` — Clears the text template content.
  - **Note**: These methods are designed for clearing fields post-send or before re-use, enabling more flexible email management.

- **Recipient Handling Changes**
  - **Changed**: Methods that previously accepted a list of recipients (e.g., `to_email`) have been updated to accept a single string (for one recipient).
  - **New**: To send emails to multiple recipients, use the `add_new_recipient()` method, which allows adding extra recipients without modifying the main recipient field.

---

### Internal Enhancements

- **Safe Defaults & Defensive Code**
  - Type checks on logger type and formatter structure and database integration.
  - Fallbacks in place to prevent crashing during development misconfigurations.

---

### Documentation & Dev Experience

- **README Improvements**
  - Full guide on how to write a custom exception formatter.
  - Notes on console vs file logging — special characters like `🔥` or `→` may not render properly in file logs.
  - Emphasis on sticking to plain Unicode-compatible characters for file output.

- **Verbose Debug Output**
  - Developer-facing messages for handler registration, formatter validation, and internal method calls.
  - Index tracking added when removing or updating logger handlers.

---

## [1.10.2] - 2025-04-24

### Added
- Updated `README.md` with clearer usage examples and PyPI download badge.
- Added a content table for easier navigation.

### Changed
- Minor formatting improvements in the documentation.

---

## [1.10.0] - 2025-04-23

### Added
- Introduced initial public release of `django-email-sender`.
- Chainable API for sending rich HTML/text emails using Django templates.
- Support for context injection, custom folders, and both plain and HTML email bodies.
