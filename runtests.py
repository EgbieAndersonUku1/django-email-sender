import os
import sys
from pathlib import Path
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent / "tests"
    sys.path.insert(0, str(Path(__file__).resolve().parent))

    if not settings.configured:
        settings.configure(
            BASE_DIR=BASE_DIR,
            DEBUG=True,
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            INSTALLED_APPS=[
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django_email_sender",
            ],
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "APP_DIRS": True,
                    "DIRS": [BASE_DIR / "templates"],

                }
            ],
            SECRET_KEY="test-secret-key-for-local-testing",
        )

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
