"""Tests for the core API."""
from django.test import TestCase
from django.urls import reverse
from collectivo.auth.clients import AuthClient


class SchemaTests(TestCase):
    """Test the public features of the core API."""

    def setUp(self):
        """Set up the test client."""
        self.client = AuthClient()
        self.client.force_roles(["superuser"])

    def test_schema(self):
        """Test getting current version is correct."""
        res = self.client.get(
            reverse("collectivo:collectivo.members.emails:campaign-schema")
        )
        self.assertEqual(res.status_code, 200)
