"""Test the features of the emails API."""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.db.models import signals
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from collectivo.tags.models import Tag
from collectivo.utils.test import create_testuser

from .models import EmailCampaign

TEMPLATES_URL = reverse("collectivo.emails:template-list")
CAMPAIGNS_URL = reverse("collectivo.emails:campaign-list")
DESIGNS_URL = reverse("collectivo.emails:design-list")

User = get_user_model()


def run_mocked_celery_chain(mocked_chain):
    """Take a called mocked celery chain and run it locally."""
    if mocked_chain.call_args:
        args = list(mocked_chain.call_args[0])
        task = args.pop(0).apply()
        for arg in args:
            task = arg.apply((task.result,))
        return task.result


class EmailsTests(TestCase):
    """Test the members emails API."""

    def setUp(self):
        """Prepare test case."""
        signals.post_save.disconnect(
            sender=User, dispatch_uid="update_keycloak_user"
        )
        self.client = APIClient()
        self.user = create_testuser(superuser=True)
        self.client.force_authenticate(self.user)
        res = self.client.post(
            DESIGNS_URL, {"name": "a great design", "body": "TEST {{content}}"}
        )
        self.tag = Tag.objects.create(name="email_test_tag")
        self.template_data = {
            "name": "a great template",
            "subject": "Test",
            "design": res.data["id"],
            "body": "First name: {{user.first_name}} <br/> New line",
            "tag__tag": self.tag.pk,
        }
        self.recipient_objects = [
            User.objects.create_user(
                username=f"recipient_0{i}@example.com",
                first_name=f"Recipient_0{i}",
                email=f"recipient_0{i}@example.com",
            )
            for i in [1, 2]
        ]
        self.recipients = [u.pk for u in self.recipient_objects]

    def _batch_assertions(self, res):
        """Assert the results of a batch email request."""
        self.assertEqual(res.status_code, 201)

        obj = EmailCampaign.objects.get(pk=res.data["id"])
        self.assertEqual(obj.status, "success")
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(
            mail.outbox[0].recipients()[0], "recipient_01@example.com"
        )
        self.assertEqual(mail.outbox[0].subject, "Test")
        self.assertEqual(
            mail.outbox[0].alternatives[0][0],
            "TEST First name: Recipient_01 <br/> New line",
        )
        self.assertEqual(
            mail.outbox[0].body,
            "TEST First name: Recipient_01  \nNew line\n\n",
        )

        # TODO: Move to emails_tags tests
        self.assertTrue(
            self.recipient_objects[0].tags.filter(pk=self.tag.pk).exists()
        )

    @patch("collectivo.emails.serializers.chain")
    def test_email_batch_template(self, chain):
        """Test sending a batch of emails using a template."""
        res = self.client.post(TEMPLATES_URL, self.template_data)
        self.assertEqual(res.status_code, 201)
        payload = {
            "send": True,
            "template": res.data["id"],
            "recipients": self.recipients,
        }
        res = self.client.post(CAMPAIGNS_URL, payload)
        self.assertEqual(res.status_code, 201)
        run_mocked_celery_chain(chain)
        self._batch_assertions(res)
