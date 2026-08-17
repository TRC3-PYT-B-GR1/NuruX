from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AccountApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='account-user',
            email='account@example.com',
            password='InitialPass!234',
        )

    def test_login_accepts_email_and_returns_identity(self):
        response = self.client.post(
            reverse('auth-login'),
            {'username': self.user.email, 'password': 'InitialPass!234'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], self.user.email)

    def test_login_accepts_case_insensitive_email_with_spaces(self):
        response = self.client.post(
            reverse('auth-login'),
            {'username': '  ACCOUNT@EXAMPLE.COM ', 'password': 'InitialPass!234'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_change_password(self):
        self.client.force_authenticate(self.user)
        url = reverse('auth-change-password')
        rejected = self.client.post(
            url,
            {'current_password': 'wrong-password', 'new_password': 'Replacement!234'},
            format='json',
        )
        self.assertEqual(rejected.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            url,
            {'current_password': 'InitialPass!234', 'new_password': 'Replacement!234'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Replacement!234'))
