"""Shifts extension for collectivo."""


from os.path import abspath, dirname

from django.apps import apps


def load_tests(loader, tests, pattern):
    """Load tests only if app is installed."""
    from django.conf import settings

    if apps.is_installed("collectivo.shifts"):
        return loader.discover(
            start_dir=dirname(abspath(__file__)), pattern=pattern
        )
