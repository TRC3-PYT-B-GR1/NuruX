"""
Permission-boundary tests for Employee CRUD.

These use APIClient.force_authenticate() rather than a real JWT login flow
deliberately — login/token mechanics are exercised separately in
apps.accounts.tests, so these tests isolate exactly one thing: does the
RBAC in EmployeeViewSet/EmployeePermission actually enforce the PRD §8
matrix. That's the highest-risk surface in this codebase (every phase after
Phase 3 builds on get_visible_employees()), so it's the one most worth
testing thoroughly.

Requires a real PostgreSQL test database (Django creates/drops it
automatically around the run) since DATABASES has no sqlite fallback —
run with: python manage.py test apps.employees
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.employees.models import Employee
from apps.organizations.models import Department, Role

User = get_user_model()


class EmployeeVisibilityTests(APITestCase):
    def setUp(self):
        self.department_a = Department.objects.create(name="Engineering")
        self.department_b = Department.objects.create(name="Finance")
        self.role = Role.objects.create(title="Officer", department=self.department_a)

        self.admin_user = User.objects.create_user(
            username="admin1", email="admin1@workforge.ng", password="pass12345", role=User.Role.SUPER_ADMIN
        )
        self.hr_user = User.objects.create_user(
            username="hr1", email="hr1@workforge.ng", password="pass12345", role=User.Role.HR_OFFICER
        )
        self.manager_user = User.objects.create_user(
            username="mgr1", email="mgr1@workforge.ng", password="pass12345", role=User.Role.MANAGER
        )
        self.employee_user = User.objects.create_user(
            username="emp1", email="emp1@workforge.ng", password="pass12345", role=User.Role.EMPLOYEE
        )
        self.other_employee_user = User.objects.create_user(
            username="emp2", email="emp2@workforge.ng", password="pass12345", role=User.Role.EMPLOYEE
        )

        self.manager_profile = Employee.objects.create(
            user=self.manager_user, first_name="Mary", last_name="Manager",
            email="mary.manager@workforge.ng", department=self.department_a,
        )
        self.team_member_profile = Employee.objects.create(
            user=self.employee_user, first_name="Eze", last_name="Emeka",
            email="eze.emeka@workforge.ng", department=self.department_a,
            manager=self.manager_profile,
        )
        self.outsider_profile = Employee.objects.create(
            user=self.other_employee_user, first_name="Bola", last_name="Bello",
            email="bola.bello@workforge.ng", department=self.department_b,
        )

        self.list_url = reverse("employee-list")

    def _ids(self, response):
        return {row["id"] for row in response.data["results"]}

    def test_hr_officer_sees_every_employee(self):
        self.client.force_authenticate(self.hr_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self._ids(response),
            {self.manager_profile.id, self.team_member_profile.id, self.outsider_profile.id},
        )

    def test_manager_sees_only_their_team_and_self(self):
        self.client.force_authenticate(self.manager_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self._ids(response),
            {self.manager_profile.id, self.team_member_profile.id},
        )
        self.assertNotIn(self.outsider_profile.id, self._ids(response))

    def test_employee_sees_only_themselves(self):
        self.client.force_authenticate(self.employee_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self._ids(response), {self.team_member_profile.id})

    def test_employee_cannot_retrieve_someone_elses_record(self):
        self.client.force_authenticate(self.employee_user)
        url = reverse("employee-detail", args=[self.outsider_profile.id])
        response = self.client.get(url)
        # 404, not 403 — get_queryset() already excludes it, so it looks
        # like it doesn't exist rather than confirming it does but is off-limits.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_employee_cannot_create_employee(self):
        self.client.force_authenticate(self.employee_user)
        payload = {
            "first_name": "New", "last_name": "Hire",
            "email": "new.hire@workforge.ng", "department": self.department_a.id,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hr_officer_can_create_employee(self):
        self.client.force_authenticate(self.hr_user)
        payload = {
            "first_name": "New", "last_name": "Hire",
            "email": "new.hire@workforge.ng", "department": self.department_a.id,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EmployeeSelfServiceTests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Ops")
        self.employee_user = User.objects.create_user(
            username="emp3", email="emp3@workforge.ng", password="pass12345", role=User.Role.EMPLOYEE
        )
        self.profile = Employee.objects.create(
            user=self.employee_user, first_name="Kate", last_name="King",
            email="kate.king@workforge.ng", department=self.department,
        )

    def test_employee_can_update_own_phone_number(self):
        self.client.force_authenticate(self.employee_user)
        url = reverse("employee-detail", args=[self.profile.id])
        response = self.client.patch(url, {"phone_number": "+2348012345678"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, "+2348012345678")

    def test_employee_cannot_change_own_department_via_self_service_fields(self):
        """
        The self-service serializer doesn't expose `department` at all, so
        attempting to set it should just be silently ignored by the
        serializer (not error, not applied) — this pins that behaviour.
        """
        other_department = Department.objects.create(name="Legal")
        self.client.force_authenticate(self.employee_user)
        url = reverse("employee-detail", args=[self.profile.id])
        response = self.client.patch(url, {"department": other_department.id, "phone_number": "0800000000"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.department_id, self.department.id)  # unchanged


class EmployeeSoftDeleteTests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Sales")
        self.admin_user = User.objects.create_user(
            username="admin2", email="admin2@workforge.ng", password="pass12345", role=User.Role.SUPER_ADMIN
        )
        self.profile = Employee.objects.create(
            first_name="Tunde", last_name="Bakare", email="tunde.bakare@workforge.ng",
            department=self.department,
        )

    def test_delete_soft_deletes_not_hard_deletes(self):
        self.client.force_authenticate(self.admin_user)
        url = reverse("employee-detail", args=[self.profile.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.status, Employee.Status.EXITED)
        self.assertIsNotNone(self.profile.exit_date)
        self.assertTrue(Employee.objects.filter(pk=self.profile.pk).exists())  # row still there
