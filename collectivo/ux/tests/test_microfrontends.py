"""Test the micro-frontend API."""

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from collectivo.ux.models import MicroFrontend


EXTENSIONS_URL = reverse('collectivo:collectivo.extensions:extension-list')
MICROFRONTEND_URL = reverse('collectivo:collectivo.ux:microfrontend-list')


class PublicExtensionsApiTests(TestCase):
    """Test the publicly available micro-frontend API."""

    def setUp(self):
        """Prepare client, extension, & micro-frontend."""
        self.client = APIClient()
        self.ext_name = 'my_extension'
        self.mf_name = 'my_microfrontend'
        self.client.post(EXTENSIONS_URL, {'name': self.ext_name})
        payload = {
            'name': self.mf_name,
            'extension': self.ext_name,
            'path': 'http://example.com',
            'type': 'components',
        }
        self.client.post(MICROFRONTEND_URL, payload)

    def test_create_microfrontend(self):
        """Test that microfrontend created in setup exists."""
        exists = MicroFrontend.objects.filter(name=self.mf_name).exists()
        self.assertTrue(exists)

    def test_delete_microfrontend_through_cascade(self):
        """Test that deleting extension also deletes microfrontend."""
        self.client.delete(EXTENSIONS_URL+self.ext_name+'/')
        exists = MicroFrontend.objects.filter(name=self.mf_name).exists()
        self.assertFalse(exists)
