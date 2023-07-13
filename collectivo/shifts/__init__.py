"""Shifts extension for collectivo."""


from os.path import abspath, dirname

from django.conf import settings


def load_tests(loader, tests, pattern):
    """Load tests only if app is installed."""
    from django.conf import settings

    if "collectivo.shifts" in settings.INSTALLED_APPS:
        return loader.discover(
            start_dir=dirname(abspath(__file__)), pattern=pattern
        )
