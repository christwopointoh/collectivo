"""Tests for the core API."""
from django.test import TestCase
from django.urls import reverse
from collectivo.version import __version__
from collectivo.auth.clients import AuthClient


class PublicCoreApiTests(TestCase):
    """Test the public features of the core API."""

    def setUp(self):
        """Set up the test client."""
        self.client = AuthClient()
        self.client.force_roles(["superuser"])

    def testGetVersion(self):
        """Test getting current version is correct."""
        res = self.client.get(reverse("collectivo:version"))
        self.assertEqual(res.data["version"], __version__)
