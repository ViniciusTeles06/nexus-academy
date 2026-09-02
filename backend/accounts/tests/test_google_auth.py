from unittest.mock import patch

from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from accounts.services.google_auth import GoogleTokenError


class GoogleLoginAPITests(APITestCase):
    def setUp(self):
        self.url = reverse("google-login")

        self.google_payload = {
            "sub": "google-user-123",
            "email": "aluno@nexus.com",
            "email_verified": True,
            "given_name": "João",
            "family_name": "Silva",
            "picture": "https://example.com/avatar.jpg",
        }

    @override_settings(GOOGLE_CLIENT_ID="")
    def test_google_login_returns_503_when_not_configured(self):
        response = self.client.post(
            self.url,
            {
                "credential": "fake-google-token",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    @override_settings(
        GOOGLE_CLIENT_ID="test-google-client-id"
    )
    @patch("accounts.views.verify_google_token")
    def test_google_login_creates_student_user(
        self,
        mock_verify_google_token,
    ):
        mock_verify_google_token.return_value = (
            self.google_payload
        )

        response = self.client.post(
            self.url,
            {
                "credential": "valid-google-token",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

        self.assertIn(
            "user",
            response.data,
        )

        user = User.objects.get(
            email="aluno@nexus.com"
        )

        self.assertEqual(
            user.role,
            User.Role.STUDENT,
        )

        self.assertEqual(
            user.first_name,
            "João",
        )

        self.assertEqual(
            user.last_name,
            "Silva",
        )

        self.assertTrue(
            user.is_email_verified
        )

        self.assertEqual(
            user.avatar,
            "https://example.com/avatar.jpg",
        )

        self.assertFalse(
            user.has_usable_password()
        )

        self.assertIn(
            settings.AUTH_COOKIE_NAME,
            response.cookies,
        )

        self.assertTrue(
            response.cookies[
                settings.AUTH_COOKIE_NAME
            ]["httponly"]
        )

    @override_settings(
        GOOGLE_CLIENT_ID="test-google-client-id"
    )
    @patch("accounts.views.verify_google_token")
    def test_google_login_reuses_existing_user(
        self,
        mock_verify_google_token,
    ):
        user = User.objects.create_user(
            email="aluno@nexus.com",
            password="SenhaForte123!",
            first_name="João",
            last_name="Silva",
            role=User.Role.TEACHER,
        )

        mock_verify_google_token.return_value = (
            self.google_payload
        )

        response = self.client.post(
            self.url,
            {
                "credential": "valid-google-token",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            User.objects.filter(
                email="aluno@nexus.com"
            ).count(),
            1,
        )

        user.refresh_from_db()

        self.assertEqual(
            user.role,
            User.Role.TEACHER,
        )

        self.assertTrue(
            user.is_email_verified
        )

    @override_settings(
        GOOGLE_CLIENT_ID="test-google-client-id"
    )
    @patch("accounts.views.verify_google_token")
    def test_google_login_rejects_invalid_token(
        self,
        mock_verify_google_token,
    ):
        mock_verify_google_token.side_effect = (
            GoogleTokenError(
                "Token do Google inválido."
            )
        )

        response = self.client.post(
            self.url,
            {
                "credential": "invalid-token",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            response.data["detail"],
            "Token do Google inválido.",
        )

    @override_settings(
        GOOGLE_CLIENT_ID="test-google-client-id"
    )
    @patch("accounts.views.verify_google_token")
    def test_google_login_rejects_inactive_user(
        self,
        mock_verify_google_token,
    ):
        user = User.objects.create_user(
            email="aluno@nexus.com",
            password="SenhaForte123!",
            role=User.Role.STUDENT,
        )

        user.is_active = False
        user.save(
            update_fields=["is_active"]
        )

        mock_verify_google_token.return_value = (
            self.google_payload
        )

        response = self.client.post(
            self.url,
            {
                "credential": "valid-google-token",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    @override_settings(
        GOOGLE_CLIENT_ID="test-google-client-id"
    )
    def test_google_login_requires_credential(self):
        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )