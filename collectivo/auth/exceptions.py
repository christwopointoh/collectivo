"""Exceptions of the authentication module."""
from rest_framework.exceptions import ParseError


class AuthDeleteError(ParseError):
    """Exception raised when deleting a user fails (HTTP 400)."""

    pass


class AuthUpdateError(ParseError):
    """Exception raised when updating a user fails (HTTP 400)."""

    pass


class AuthCreateError(ParseError):
    """Exception raised when creating a user fails (HTTP 400)."""

    pass


class AuthGetError(ParseError):
    """Exception raised when getting a user fails (HTTP 400)."""

    pass
