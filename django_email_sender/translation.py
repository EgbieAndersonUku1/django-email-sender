# Supported languages (ISO 639-1 codes):
# - es: Spanish
# - fr: French
# - de: German
# - it: Italian
# - pt: Portuguese
# - ru: Russian
# - zh: Simplified Chinese
# - ja: Japanese
# - ko: Korean
# - nl: Dutch
# - ar: Arabic
# These are the languages currently available for translation in the application.


from django.conf import settings
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from logging import Logger, LoggerAdapter
from typing import Optional


DEFAULT_LANGUAGE    = "en"
SUPPORTED_LANGUAGES = {'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko', 'nl', 'ar'}


_cached_lang_code: Optional[str] = None  


def is_django_ready() -> bool:
    """
    Checks if Django is fully initialized and ready using the app registry.
    """
    try:
        # Ensure Django apps are fully loaded
        return apps.ready
    except ImproperlyConfigured:
        return False
    

def detect_user_language() -> str:
    """
    Detect the user's preferred language.
    """
    global _cached_lang_code

    if _cached_lang_code is not None:
        return _cached_lang_code

    lang_code = getattr(settings, "LANGUAGE_CODE", DEFAULT_LANGUAGE)

    parsed_lang_code = parse_user_language(lang_code)

    if parsed_lang_code not in SUPPORTED_LANGUAGES:
        _cached_lang_code = DEFAULT_LANGUAGE
    else:
        _cached_lang_code = parsed_lang_code

    return _cached_lang_code


def parse_user_language(lang_code: Optional[str]) -> Optional[str]:
    """
    Parse and normalize the language code.
    """
    if not lang_code or not isinstance(lang_code, str):
        return None

    return lang_code.split("-")[0].split("_")[0].lower()




def set_language(logger: Optional[Logger] = None) -> None:
    """
    Set the language for the current session.
    Logs the language activation process if logger is provided.
    """
    lang_code = detect_user_language()
    if logger:
        logger.info(_("Setting language to {}".format(lang_code)))
    
    translation.activate(lang_code)


def translate_message(msg: str, *args, **kwargs) -> str:
    """Safely translate and format a message."""
    try:
        if msg:
            if args or kwargs:
                return msg.format(*args, **kwargs)
            return msg
    except (IndexError, KeyError):
        return msg
    except Exception:
        return msg


def safe_set_language(logger: Optional[Logger] = None) -> None:
    """
    Safely activate language only if Django is fully ready.
    """

    # Validate logger type
    if logger is not None:
        if not isinstance(logger, (Logger, LoggerAdapter)):
            error_msg = _("The logger passed is not an instance of the Logger class. Expected an instance but got {logger_type}")
            raise TypeError(translate_message(error_msg, logger_type=type(logger)))

    if is_django_ready():
        if logger:
            logger.info(_("Setting language safely..."))
            logger.info(_("Django is ready, activating language."))

        try:
            set_language(logger=logger)
        except Exception as e:
            if logger:
                logger.error(translate_message(_("Error activating language: {activation_error}"), activation_error=str(e)))
            raise
    else:
        if logger:
            logger.warning(_("Django is not ready, skipping language activation."))
