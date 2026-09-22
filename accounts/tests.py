from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LogoutTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="owner", password="Strong-test-pass-2026")

    def test_logout_is_post_only_and_invalidates_session(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertEqual(response["Cache-Control"], "no-store, no-cache, must-revalidate, max-age=0")
        self.assertNotIn("_auth_user_id", self.client.session)
        private_response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(private_response.status_code, 302)
