from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.organizations.models import Department, Role
from .models import Employee

User = get_user_model()


class EmployeeSecurityTests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Finance')
        self.role = Role.objects.create(title='Analyst', department=self.department)
        self.hr = User.objects.create_user(
            username='hr', email='hr@example.com', password='ValidPass!234', role='hr_officer'
        )
        self.regular_user = User.objects.create_user(
            username='regular', email='regular@example.com', password='ValidPass!234'
        )

    def payload(self, email='new@example.com', role='employee'):
        return {
            'first_name': 'New',
            'last_name': 'Hire',
            'email': email,
            'password': 'ValidPass!234',
            'department': self.department.id,
            'role': self.role.id,
            'rbac_role': role,
        }

    def test_regular_employee_cannot_create_employee(self):
        self.client.force_authenticate(self.regular_user)
        response = self.client.post(reverse('employee-list'), self.payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hr_can_create_employee_but_not_super_admin(self):
        self.client.force_authenticate(self.hr)
        forbidden = self.client.post(
            reverse('employee-list'), self.payload(role='super_admin'), format='json'
        )
        self.assertEqual(forbidden.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(
            reverse('employee-list'), self.payload(email='allowed@example.com'), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee = Employee.objects.get(user__email='allowed@example.com')
        self.assertEqual(employee.user.role, 'employee')
        self.assertEqual(
            self.client.delete(reverse('employee-detail', args=[employee.pk])).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
