## ✅ VERSION\_HISTORY.md


### 📦 Version History

---

## 2.0.0 — 2025-05-11

### ✨ Major Changes
- Introduced `EmailSenderLogger` class for advanced logging and optional database integration.
- All core functionality is now chainable.
- Added `.clear_to()`, `.clear_subject()`, and similar methods for better control over email state.
- `.to()` now accepts a string (not a list); use `.add_new_recipient()` for multiple recipients.
- Logging must now be explicitly started with `.start_logging_session()` to prevent unintentional logging.
- To save to database even adding a custom model, you must call `.enable_email_meta_data_save()`, this ensures unintentional database entry

### 🛠️ Improvements
- Fielderror handling for missing fields and misconfiguration.
- Email payload logging includes metadata, payload and summary.
- Email tracking summary report

---

## [1.10.2] - 2025-04-24

### Added
- Updated `README.md` with clearer usage examples and PyPI download badge.
- Added a content table for easier navigation.
- Updated it with the new features added.

### Changed
- Minor formatting improvements in the documentation.
-
---



## [1.10.0] - 2025-04-23

### Added
- Introduced initial public release of `django-email-sender`.
- Chainable API for sending rich HTML/text emails using Django templates.
- Support for context injection, custom folders, and both plain and HTML email bodies.


---

## 🔄 Migration Notes (Add to README or `MIGRATION.md`)


### 🔄 Migrating from v1.x to v2.0.0

The 2.0.0 release includes structural changes, new featues, database and logging integration, maintainability, etc. If you're upgrading, here’s what to update:

---

### ✅ `EmailSender` Changes
- `to()` now accepts a string:  
  `EmailSender().to("user@example.com")`  
  ✅ Old: `.to(["user@example.com"])` ❌

- To send to multiple people, use `.add_new_recipient("email@example.com")`.

- You can now clear values with methods like `.clear_subject()` and `.clear_to()`.

---

### ✅ Introducing `EmailSenderLogger`
- Use this class if you want:
  - Email sending logs
  - Metadata and payload logging
  - Optional database persistence
  - Centralised logging configuration
  - database integration
  - logger integration
  - Full report summary regarding email delivery
  - Add custom formatter for error reporting


```python
EmailSenderLogger(email_sender_instance)
    .start_logging_session()

    # ... additional fields here
    .send()
````

* If you don’t need logging, just keep using `EmailSender` as before or use `EmailSenderLogger` powered with the instance of `EmailSender`.

---

### ✅ Logging Behaviour

* Logging is opt-in. To enable logging:

```python
email_logger.start_logging_session()
```

If omitted, log output will state:

```plaintext
[Logger Not Enabled: Logger is not enabled. Skipping logging.]
```

### ✅ Database Behaviour

* Database is opt-in. To enable dabase:

```python
email_logger.add_log_model(CustomLogModel)
.enable_email_meta_data_save()
```
If omitted, no metadata will be added to the database





---