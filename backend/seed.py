import os
import django
import sys
from datetime import datetime, timedelta
from django.utils import timezone

sys.path.append('c:/Users/USER/NuruX/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User, Department
from employees.models import Employee
from attendance.models import Attendance
from leave.models import LeaveRequest
from rest_framework_simplejwt.tokens import RefreshToken

# Clear existing
User.objects.all().delete()
Department.objects.all().delete()

# Departments (Googleplex coords approx 37.422, -122.084)
eng = Department.objects.create(name="Engineering", latitude=37.422, longitude=-122.084)
design = Department.objects.create(name="Design", latitude=37.422, longitude=-122.084)

# Users
manager_user = User.objects.create_user(username="evan", email="evan@nurux.com", password="password", first_name="Evan", last_name="Manager", role="HR")
emp1_user = User.objects.create_user(username="sarah", email="sarah@nurux.com", password="password", first_name="Sarah", last_name="Johnson", role="EMPLOYEE")
emp2_user = User.objects.create_user(username="michael", email="michael@nurux.com", password="password", first_name="Michael", last_name="James", role="EMPLOYEE")
emp3_user = User.objects.create_user(username="david", email="david@nurux.com", password="password", first_name="David", last_name="Okoro", role="EMPLOYEE")
emp4_user = User.objects.create_user(username="grace", email="grace@nurux.com", password="password", first_name="Grace", last_name="Williams", role="EMPLOYEE")

# Employees
Employee.objects.create(user=manager_user, department=eng, role_title="Engineering Manager")
emp1 = Employee.objects.create(user=emp1_user, department=eng, role_title="Software Engineer")
emp2 = Employee.objects.create(user=emp2_user, department=design, role_title="UI/UX Designer")
emp3 = Employee.objects.create(user=emp3_user, department=eng, role_title="Backend Developer")
emp4 = Employee.objects.create(user=emp4_user, department=design, role_title="Product Designer")

# Attendance for today
today = timezone.now().date()
# Valid clock in
Attendance.objects.create(employee=emp1, date=today, clock_in=timezone.now().replace(hour=7, minute=54), status=Attendance.Status.PRESENT, gps_location_in="37.422,-122.084")
# Valid clock in
Attendance.objects.create(employee=emp3, date=today, clock_in=timezone.now().replace(hour=8, minute=26), status=Attendance.Status.PRESENT, gps_location_in="37.4225,-122.0845")
# Anomaly clock in (far away)
Attendance.objects.create(employee=emp4, date=today, clock_in=timezone.now().replace(hour=9, minute=15), status=Attendance.Status.PRESENT, gps_location_in="37.7749,-122.4194", is_anomaly=True, anomaly_reason="GPS LOCATION MISMATCH: Detected 48.2 km away from office.")
# Late
Attendance.objects.create(employee=emp2, date=today, status=Attendance.Status.LATE)

# Leave Requests
LeaveRequest.objects.create(
    employee=emp1, 
    leave_type="ANNUAL", 
    start_date=today + timedelta(days=5), 
    end_date=today + timedelta(days=6), 
    reason="Vacation", 
    status="PENDING"
)

LeaveRequest.objects.create(
    employee=emp2, 
    leave_type="SICK", 
    start_date=today + timedelta(days=2), 
    end_date=today + timedelta(days=3), 
    reason="Medical appointment", 
    status="PENDING"
)

# Generate Token
refresh = RefreshToken.for_user(manager_user)
print(f"ACCESS_TOKEN={str(refresh.access_token)}")
