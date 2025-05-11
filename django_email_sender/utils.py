import json
import inspect


from django.utils.encoding import force_str
from django.utils.functional import Promise
from time import perf_counter
from pathlib import Path
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from dataclasses import dataclass
from bs4 import BeautifulSoup

from django_email_sender.translation import translate_message



def get_template_dirs():
    """
    Retrieves the paths for the template directories used by the application.

    This function checks for the custom template directory setting in Django's
    settings (`MYAPP_TEMPLATES_DIR`). If the custom setting is not found, it falls
    back to the default location: `BASE_DIR / 'templates'`.

    The function constructs the path for email templates under the `emails_templates`
    subdirectory inside the templates directory.

    Raises:
        ImproperlyConfigured: If the `BASE_DIR` setting is not defined in Django settings.

    Returns:
        dict: A dictionary containing the following template directory paths:
            - 'BASE_DIR': The base directory of the Django project.
            - 'TEMPLATES_DIR': The directory where templates are stored, either custom or default.
            - 'EMAIL_TEMPLATES_DIR': The directory where email templates are stored, inside the `TEMPLATES_DIR`.
    """
    try:
        base_dir = getattr(settings, "BASE_DIR")
    except AttributeError:
        raise ImproperlyConfigured("settings.BASE_DIR is not defined. Please define it in settings.py.")

    # Get the custom template directory path or fall back to the default
    templates_dir = getattr(settings, "MYAPP_TEMPLATES_DIR", Path(base_dir) / "templates")
    
    # Define the path for email templates inside the templates directory
    email_templates_dir = templates_dir / "emails_templates"

    return {
        "BASE_DIR": base_dir,
        "TEMPLATES_DIR": templates_dir,
        "EMAIL_TEMPLATES_DIR": email_templates_dir,
    }



@dataclass(frozen=True)
class MethodForDebug:
        
    CURRENT_METHOD: str
    CLASS_NAME :str
    LINE_NUMBER : int 
  
  


def mark_method_for_debugging(depth: int = 1) -> MethodForDebug:
    """
    Captures contextual information about a calling method for debugging or structured logging.

    Args:
        depth (int): The number of stack levels to go back to find the calling context.
                     Use depth=1 for direct callers (default), depth=2 for wrapper/helper methods, etc.

    Returns:
        MethodForDebug: An instance containing:
            - CURRENT_METHOD: Name of the method at the specified stack depth.
            - CLASS_NAME: Name of the class (if available) or 'Dummy' otherwise.
            - LINE_NUMBER: The line number in the source where this function was called.

    Notes:
        - This function introspects the call stack to extract runtime context using `inspect`.
        
        - It must be called from within the method whose debug info is required,
          or with appropriate `depth` if used in wrappers.
          
        - Internal frame references are explicitly deleted to avoid reference cycles
          and potential memory leaks.
        
        - Be cautious with depth > 1, especially in complex call stacks.

    Example:
        
        # Called without a depth call and without a depth call
        
        class Example:
            def method(self):
                debug_info = mark_method_for_debugging()
                print(debug_info)

        # When using a wrapper/helper method
        
        class WrappedExample:
            def log_debug(self):
                return mark_method_for_debugging(depth=2)

            def some_method(self):
                debug_info = self.log_debug()
                print(debug_info)
                
    
    Exampe 3 wrapper used without a depth call
    
    Example (Correct Usage 'logs' `one` and `two` ):
        class CorrectWayClass:
            def one(self):
                debug = mark_method_for_debugging()
                print(debug)

            def two(self):
                debug = mark_method_for_debugging()
                print(debug)

    Example (Incorrect Usage — logs `use_debug` instead of `one` or `two`):
        class IncorrectWayClass:
            def one(self):
                debug = self.use_debug()
                print(debug)

            def two(self):
                debug = self.use_debug()
                print(debug)

            def use_debug(self):
                return mark_method_for_debugging()
    """
    frame = inspect.currentframe()
    try:
        for _ in range(depth):
            if frame is not None:
                frame = frame.f_back

        if frame is None:
            return MethodForDebug(CURRENT_METHOD="Unknown", CLASS_NAME="Unknown", LINE_NUMBER=-1)

        method_name = frame.f_code.co_name
        class_name = frame.f_locals.get('self', type('Dummy', (), {})).__class__.__name__
        line_number = frame.f_lineno

        return MethodForDebug(
            CURRENT_METHOD=method_name,
            CLASS_NAME=class_name,
            LINE_NUMBER=line_number
        )
    finally:
        # Clean up to prevent memory leaks
        del frame


def get_safe_text_preview(body: str, length: int = 100) -> str:
    """
    Generates a safe preview of a plain text email body.

    Args:
        body (str): The plain text email body.
        length (int): Maximum length of the preview.

    Returns:
        str: A cleaned-up preview string of the text body.
    """
    preview = body.strip().replace('\n', ' ').replace('\r', '')
    return (preview[:length] + '...') if len(preview) > length else preview


def get_html_preview(html: str, length: int = 100) -> str:
    """
    Extracts and generates a safe preview of an HTML email body.

    Args:
        html (str): The HTML email content.
        length (int): Maximum length of the text preview extracted from HTML.

    Returns:
        str: A text-only preview derived from the HTML body.
    """
    text = BeautifulSoup(html, "html.parser").get_text(separator=' ', strip=True)
    return (text[:length] + '...') if len(text) > length else text


def measure_duration(func, *args, **kwargs):
    if not callable(func):
        raise TypeError("The function must be callable")

    start  = perf_counter()
    result = func(*args, **kwargs)
    end    = perf_counter()

    elapsed_time = end - start
    return result, elapsed_time




def sanitize_for_json(obj):
    """
    Recursively convert an object into something that can be safely serialized by json.dumps.
    Handles:
    - Lazy translation objects (__proxy__)
    - Sets (converted to lists)
    - Custom objects (via str fallback)
    """
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        return [sanitize_for_json(v) for v in obj]
    elif isinstance(obj, Promise):
        return force_str(obj)
    elif isinstance(obj, (int, float, bool)) or obj is None:
        return obj
    else:
        try:
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            return force_str(obj)
