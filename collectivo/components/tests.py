"""Tests of the components module."""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from collectivo.utils.test import create_testuser

EXTENSIONS_URL = reverse("collectivo.components:component-list")


class ComponentsTests(TestCase):
    """Test the components extension."""

    def setUp(self):
        """Prepare test case."""
        self.client = APIClient()
        self.user = create_testuser(superuser=True)
        self.client.force_authenticate(self.user)
