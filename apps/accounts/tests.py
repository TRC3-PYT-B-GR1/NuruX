"""
Auth-flow tests: login, account lockout after repeated failures, and the
Phase 6 role-management endpoint.

Run with: python manage.py test apps.accounts
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.audit.models import AuditLog

User = get_user_model()


class LoginAndLockoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="locktest", email="locktest@workforge.ng", password="correct-password", role=User.Role.EMPLOYEE
        )
        self.login_url = reverse("auth-login")

    def test_successful_login_returns_tokens(self):
        response = self.client.post(self.login_url, {"username": "locktest", "password": "correct-password"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_wrong_password_does_not_lock_account_before_threshold(self):
        self.client.post(self.login_url, {"username": "locktest", "password": "wrong"})
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_locked)
        self.assertEqual(self.user.failed_login_attempts, 1)

    def test_account_locks_after_max_failed_attempts(self):
        for _ in range(settings.MAX_FAILED_LOGIN_ATTEMPTS):
            self.client.post(self.login_url, {"username": "locktest", "password": "wrong"})

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_locked)

        # Even the CORRECT password should now be rejected while locked.
        response = self.client.post(self.login_url, {"username": "locktest", "password": "correct-password"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lockout_writes_an_audit_log_entry(self):
        for _ in range(settings.MAX_FAILED_LOGIN_ATTEMPTS):
            self.client.post(self.login_url, {"username": "locktest", "password": "wrong"})

        entry = AuditLog.objects.filter(action="user.account_locked", target_id=str(self.user.pk)).first()
        self.assertIsNotNone(entry)

    def test_successful_login_resets_failed_attempt_counter(self):
        self.client.post(self.login_url, {"username": "locktest", "password": "wrong"})
        self.client.post(self.login_url, {"username": "locktest", "password": "correct-password"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 0)


class UserRoleUpdateTests(APITestCase):
    def setUp(self):
        self.super_admin = User.objects.create_user(
            username="rootuser", email="rootuser@workforge.ng", password="pass12345", role=User.Role.SUPER_ADMIN
        )
        self.hr_user = User.objects.create_user(
            username="hruser", email="hruser@workforge.ng", password="pass12345", role=User.Role.HR_OFFICER
        )
        self.target_user = User.objects.create_user(
            username="targetuser", email="targetuser@workforge.ng", password="pass12345", role=User.Role.EMPLOYEE
        )
        self.url = reverse("auth-user-role-update", args=[self.target_user.id])

    def test_super_admin_can_change_role(self):
        self.client.force_authenticate(self.super_admin)
        response = self.client.patch(self.url, {"role": "manager"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.target_user.refresh_from_db()
        self.assertEqual(self.target_user.role, "manager")

    def test_hr_officer_cannot_change_role(self):
        """
        Deliberately narrower than the FULL_WRITE_ROLES pattern used
        elsewhere — see UserRoleUpdateView's docstring for why.
        """
        self.client.force_authenticate(self.hr_user)
        response = self.client.patch(self.url, {"role": "manager"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_role_change_writes_an_audit_log_entry(self):
        self.client.force_authenticate(self.super_admin)
        self.client.patch(self.url, {"role": "director"})
        entry = AuditLog.objects.filter(action="user.role_changed", target_id=str(self.target_user.pk)).first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.changes["role"]["to"], "director")
