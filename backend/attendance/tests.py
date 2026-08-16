from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from apps.employees.models import Employee
from apps.organizations.models import Department, Role
from .models import Attendance

User = get_user_model()


class AttendanceApiTests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name='Engineering',
            latitude='6.524400',
            longitude='3.379200',
            geofence_radius_meters=200,
        )
        role = Role.objects.create(title='Engineer', department=self.department)
        self.user = User.objects.create_user(
            username='employee', email='employee@example.com', password='ValidPass!234'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Employee',
            department=self.department,
            role=role,
        )
        self.client.force_authenticate(self.user)

    def qr_token(self):
        token = AccessToken()
        token['type'] = 'attendance_qr'
        token['department_id'] = self.department.id
        return str(token)

    def test_clock_in_is_dedicated_and_cannot_be_repeated_or_deleted(self):
        response = self.client.post(
            reverse('attendance-clock-in'),
            {'gps_location': '6.524400,3.379200', 'qr_token': self.qr_token()},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        attendance = Attendance.objects.get(employee=self.employee)
        self.assertIsNotNone(attendance.clock_in)

        duplicate = self.client.post(
            reverse('attendance-clock-in'),
            {'gps_location': '6.524400,3.379200', 'qr_token': self.qr_token()},
            format='json',
        )
        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)
        delete = self.client.delete(reverse('attendance-detail', args=[attendance.pk]))
        self.assertEqual(delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_clock_out_records_geofence_anomaly(self):
        self.client.post(
            reverse('attendance-clock-in'),
            {'gps_location': '6.524400,3.379200', 'qr_token': self.qr_token()},
            format='json',
        )
        response = self.client.post(
            reverse('attendance-clock-out'),
            {'gps_location': '7.500000,4.500000', 'qr_token': self.qr_token()},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_anomaly'])
        self.assertIsNotNone(response.data['clock_out'])
