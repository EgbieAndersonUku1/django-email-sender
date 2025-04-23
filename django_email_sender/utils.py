from pathlib import Path
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured



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
