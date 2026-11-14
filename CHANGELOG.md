# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-11-13

### Added

- **Optional idempotency key support:** Added `.with_idempotency_key(idempotency_key)` to `EmailSender` and `EmailSenderLogger`. It accepts a `str` or `uuid.UUID` and stores the value as a string.
  - When a non-empty key is configured, outgoing emails include an `X-Idempotency-Key` header.
  - Added `idempotency_key` to `EmailPayload` and `EmailSenderConstants.Fields.IDEMPOTENCY_KEY` for payload inspection and audit logging.
  - Invalid argument types raise `InvalidIdempotencyKey`.
  - **Important:** The header does **not** prevent duplicate sends by itself. Deduplication, retry coordination, and persistence are the consuming application's responsibility (for example, through an application-owned `EmailOutbox` model).

- **Tests and test runner:** Added `runtests.py` and tests in `tests/test_email_sender.py` and `tests/test_email_logger.py` for sending, idempotency headers, logger payloads, field resets, and error handling.
  - Expanded recipient regression coverage for `.to()` string/list compatibility, `.add_new_recipient()` chaining and uniqueness, and duplicate removal when the primary recipient also appears among additional recipients.

- **Documentation:** Updated `README.md`, `usage.md`, `VERSION_HISTORY.md`, and `docs/index.md` with v2.1.0 API details, recipient-handling behaviour, examples, and application-managed idempotency guidance.
  - Updated the Read the Docs documentation for v2.1.0.
  - Fixed broken internal documentation references.
  - Verified that the Sphinx HTML documentation builds successfully without warnings.

### Changed

- **Python compatibility:** Updated `setup.py` to declare `python_requires=">=3.10,<3.14"`, including Python 3.13 in the supported range.

- **Method contract validation:** Updated `_types_match` and `validate_method_signature` in `validation.py` to handle Python 3.10+ union annotations (`str | uuid.UUID`), `Optional`, and `typing.Dict` generics.

### Fixed

- Fixed `EmailSender.clear_all_fields()` using `Fields` enum members instead of their `.value` strings with `setattr()`, including the `send(auto_reset=True)` path.

- Corrected invalid-key exception formatting in `EmailSenderLogger.with_idempotency_key()` (`type(key).__name__` → `type(idempotency_key).__name__`).

- Removed a duplicate `'key'` dictionary entry in `get_email_sender_param_contract()` for `IDEMPOTENCY_KEY`.

- Fixed `EmailSenderLogger.payload` omitting `idempotency_key` when `auto_reset=False`.

- **Recipient deduplication:** Fixed duplicate recipient addresses when the primary recipient was also added through `.add_new_recipient()`. Recipients are now deduplicated before sending, preserving the primary recipient first. Additional recipient ordering is not guaranteed because additional addresses are stored in a set.

### Testing

Run the project's test suite from the repository root:

```bash
python runtests.py
```

The latest reported local run completed successfully: **20 tests passed** (2026-11-13).

The Sphinx documentation build also completed successfully without warnings:

```bash
python -m sphinx -b html docs docs/_build/html -E -W --keep-going
```

---

## [2.0.5]

### Changed

- Improved the `FIELD_HAS_BEEN_CLEARED` message to report the field name, previous value, and current value more clearly.
- Centralized individual field-clearing logic in `self._clear_and_log_field(field_name, current_value)`.
- Updated `_log_field_cleared_message()` to accept `previous_value` and `current_value`.

### Fixed

- Fixed a runtime error when calling `send()` without `auto_reset=True`.

---

## [2.0.3]

### Added

- Restored backward compatibility in `EmailSender.to()` for string or list inputs. For a non-empty list, only the **first** address is used as the primary recipient; use `.add_new_recipient()` to add more recipients.
- Expanded the `.to()` docstring to explain this behaviour.

### Documentation

- Updated `README.md` to clarify recipient-list compatibility, including the historical distinction noted for `EmailSenderLogger`.

---

## [2.0.0] - 2025-05-11

### Added

- **Optional database logging:** Added support for application-provided models through dependency injection; no concrete database model is imposed.
- **Optional custom exception formatter:** Accepts a callable taking an exception and optionally a traceback, returning a string.
- **Chainable clearing methods:** Added `.clear_all_fields()`, `.clear_context()`, `.clear_from_email()`, `.clear_to_email()`, `.clear_subject()`, `.clear_html_template()`, and `.clear_text_template()` to support reusing an email sender.
- **Multiple-recipient support:** Added `.add_new_recipient()` to add recipients without replacing the primary address.

### Changed

- **Recipient API:** The v2.0.0 change encouraged a single string for `.to()`; list-input compatibility was subsequently restored in v2.0.3. See the v2.0.3 entry for current behaviour.

### Internal Improvements

- Added defensive checks for logger types, formatter configuration, and database integration.
- Improved developer-facing diagnostics for handler registration, formatter validation, and internal calls.

### Documentation

- Expanded guidance for custom exception formatters and console/file logging, including character-encoding considerations.

---

## [1.10.2] - 2025-04-24

### Added

- Improved `README.md` usage examples, PyPI download badge, and table of contents.

### Changed

- Minor documentation formatting improvements.

---

## [1.10.0] - 2025-04-23

### Added

- Initial public release of `django-email-sender`.
- Chainable API for Django template-based HTML and plain-text email.
- Template context injection and custom template folders.
