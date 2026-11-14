# 📦 Version History

## 2.1.0 — 2026-11-13

### ✨ Added

- Added `.with_idempotency_key(idempotency_key)` to both `EmailSender` and `EmailSenderLogger`. It accepts a `str` or `uuid.UUID`.
- When a non-empty idempotency key is provided, outgoing emails include the `X-Idempotency-Key` header. The key can be used by consuming applications to correlate retries and implement their own deduplication.
- Added `idempotency_key` to `EmailPayload` and `EmailSenderConstants.Fields.IDEMPOTENCY_KEY` for logging and payload inspection.
- Added Python 3.13 support (`python_requires=">=3.10,<3.14"`).

### 🛠️ Improvements & Bug Fixes

- Updated method-signature validation (`_types_match` and `validate_method_signature`) to handle Python 3.10+ union annotations (`str | uuid.UUID`), `Optional`, and `typing.Dict` generics.
- Fixed `EmailSender.clear_all_fields()` to resolve `Fields` enum members through `.value`, including when `send(auto_reset=True)` is used.
- Fixed error-message formatting in `EmailSenderLogger.with_idempotency_key()` for invalid argument types.
- Fixed `EmailSenderLogger.payload` to include `idempotency_key` when `auto_reset=False`.
- Removed a duplicate `key` dictionary entry from the idempotency-key parameter contract.
- Fixed duplicate recipient addresses when the primary address was also added using `.add_new_recipient()`; the primary address remains first.

### 📚 Documentation

- Updated `README.md`, `usage.md`, `VERSION_HISTORY.md`, and `docs/index.md` for v2.1.0.
- Verified that the Sphinx HTML documentation builds without warnings.

### 🧪 Running Tests

From the repository root, run:

```bash
python runtests.py
```

The latest reported local run passed 20 tests (2026-11-13).

**Idempotency design note:** DjangoEmailSender attaches and logs idempotency keys; it does **not** store processed keys or suppress repeated sends. Applications can implement duplicate detection with their own `EmailOutbox` model, database uniqueness constraints, or other coordination mechanism.

---

## 2.0.5

### Changed

- Improved the `FIELD_HAS_BEEN_CLEARED` message to show the field name, previous value, and current value.
- Centralized field-clearing logic in `_clear_and_log_field()` and updated `_log_field_cleared_message()`.

### Fixed

- Fixed a runtime error when calling `send()` without `auto_reset=True`.

---

## 2.0.3

### Added

- Restored backward compatibility for `EmailSender.to()` with a string or list. Only the first address in a non-empty list is used as the primary recipient; use `.add_new_recipient()` for additional addresses.

### Documentation

- Clarified recipient-list compatibility in `README.md`.

---

## 2.0.0 — 2025-05-11

### ✨ Major Changes

- Introduced `EmailSenderLogger` for logging and optional database integration.
- Expanded the chainable API, including field-clearing methods such as `.clear_subject()` and `.clear_to_email()`.
- Updated `.to()` to accept a single email-address string while retaining list input for backward compatibility (only the first list item is used). Use `.add_new_recipient()` for additional recipients.
- Made logging opt-in through `.start_logging_session()`.
- Made database persistence opt-in through `.enable_email_meta_data_save()`, with `.add_log_model()` available for custom models.

### 🛠️ Improvements

- Improved error handling for missing fields and configuration problems.
- Expanded email payload logging with metadata, payload details, and summaries.
- Added email tracking summaries.

---

## 1.10.2 — 2025-04-24

### Added

- Improved `README.md` examples, added a PyPI download badge, and expanded the table of contents.
- Updated documentation for newly introduced features.

### Changed

- Made minor documentation and formatting improvements.

---

## 1.10.0 — 2025-04-23

### Added

- Initial public release of `django-email-sender`.
- Chainable API for rich HTML and plain-text emails using Django templates.
- Template context injection and support for custom template folders.

---

## 🔄 Migration Notes

### Migrating from v1.x to v2.0.0

Version 2.0.0 introduced API changes, optional logging and database integration, and improved field management.

#### `EmailSender` changes

**Recipient compatibility:** `.to()` accepts a string or a list of strings. For backward compatibility, a list is accepted but **only its first address is used**. Use `.add_new_recipient()` for additional recipients.

```python
sender = EmailSender.create().to("user@example.com")
```

To add recipients, use `.add_new_recipient()`:

```python
sender = (
    EmailSender.create()
    .to("user@example.com")
    .add_new_recipient("another@example.com")
)
```

You can clear previously configured values with methods such as `.clear_subject()` and `.clear_to_email()`.

#### Introducing `EmailSenderLogger`

`EmailSenderLogger` provides optional email logging, payload inspection, custom logging configuration, summaries, and database persistence. To enable a logging session:

```python
email_logger = (
    EmailSenderLogger.create()
    .add_email_sender_instance(EmailSender.create())
    .start_logging_session()
)

# Configure the email fields and logger before calling .send().
```

If you do not need logging, you can continue using `EmailSender` directly.

#### Logging behaviour

Logging is opt-in. Call:

```python
email_logger.start_logging_session()
```

Without an active logging session, logger output is skipped. For details, see the README logging reference.

#### Database behaviour

Database persistence is also opt-in. If you use a custom log model, configure it and enable persistence:

```python
email_logger = (
    email_logger
    .add_log_model(CustomLogModel)
    .enable_email_meta_data_save()
)
```

Without enabling database persistence, email metadata is not saved by this feature.

### Migrating from v2.0.0 to v2.1.0

No idempotency key is required for existing email-sending calls. To attach a key to a new send operation:

```python
import uuid

operation_key = uuid.uuid4()

sender = EmailSender.create().with_idempotency_key(operation_key)
# Configure sender, recipients, subject and templates before calling .send().
```

Reuse the **same key** for retries of the same logical operation. DjangoEmailSender sends the header but does not perform duplicate detection; the consuming application is responsible for storing and checking keys when it needs that behaviour.
