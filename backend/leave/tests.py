from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.employees.models import Employee
from apps.organizations.models import Department, Role
from .models import LeaveBalance, LeaveRequest, LeaveType

User = get_user_model()


class LeaveWorkflowTests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Operations')
        role = Role.objects.create(title='Officer', department=self.department)
        self.employee_user = User.objects.create_user(
            username='worker', email='worker@example.com', password='ValidPass!234'
        )
        self.employee = Employee.objects.create(
            user=self.employee_user,
            first_name='Leave',
            last_name='Tester',
            department=self.department,
            role=role,
        )
        self.manager_user = User.objects.create_user(
            username='manager', email='manager@example.com', password='ValidPass!234', role='manager'
        )
        Employee.objects.create(
            user=self.manager_user,
            first_name='Team',
            last_name='Manager',
            department=self.department,
            role=role,
        )
        self.hr_user = User.objects.create_user(
            username='hr', email='hr@example.com', password='ValidPass!234', role='hr_officer'
        )
        self.start_date = date(date.today().year + 1, 1, 10)
        self.end_date = date(date.today().year + 1, 1, 11)
        self.balance = LeaveBalance.objects.create(
            employee=self.employee,
            leave_type=LeaveType.ANNUAL,
            year=self.start_date.year,
            total_allocated=5,
        )

    def test_two_stage_approval_deducts_balance_once(self):
        self.client.force_authenticate(self.employee_user)
        response = self.client.post(
            reverse('leave-request-list'),
            {
                'leave_type': LeaveType.ANNUAL,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'reason': 'Family commitment',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        request_id = response.data['id']

        self.client.force_authenticate(self.manager_user)
        manager_response = self.client.post(
            reverse('leave-request-approve-manager', args=[request_id]),
            {'action': 'APPROVE'},
            format='json',
        )
        self.assertEqual(manager_response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.hr_user)
        hr_url = reverse('leave-request-approve-hr', args=[request_id])
        hr_response = self.client.post(hr_url, {'action': 'APPROVE'}, format='json')
        self.assertEqual(hr_response.status_code, status.HTTP_200_OK)
        self.balance.refresh_from_db()
        self.assertEqual(self.balance.used_days, 2)
        self.assertEqual(hr_response.data['status'], LeaveRequest.Status.APPROVED_BY_HR)

        repeated = self.client.post(hr_url, {'action': 'APPROVE'}, format='json')
        self.assertEqual(repeated.status_code, status.HTTP_409_CONFLICT)
        self.balance.refresh_from_db()
        self.assertEqual(self.balance.used_days, 2)

    def test_request_requires_sufficient_allocated_balance(self):
        self.balance.total_allocated = 1
        self.balance.save(update_fields=['total_allocated'])
        self.client.force_authenticate(self.employee_user)
        response = self.client.post(
            reverse('leave-request-list'),
            {
                'leave_type': LeaveType.ANNUAL,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'reason': 'Family commitment',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
