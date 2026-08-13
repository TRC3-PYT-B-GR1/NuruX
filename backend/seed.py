import os
import django
import sys
from datetime import datetime, timedelta
from django.utils import timezone

sys.path.append('c:/Users/USER/NuruX/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.organizations.models import Department, Role
from apps.employees.models import Employee
from attendance.models import Attendance
from leave.models import LeaveRequest
from rest_framework_simplejwt.tokens import RefreshToken

# Clear existing
User.objects.all().delete()
Department.objects.all().delete()
Role.objects.all().delete()
Employee.objects.all().delete()
Attendance.objects.all().delete()
LeaveRequest.objects.all().delete()

# Departments (Googleplex coords approx 37.422, -122.084)
eng = Department.objects.create(name="Engineering", latitude=37.422, longitude=-122.084)
design = Department.objects.create(name="Design", latitude=37.422, longitude=-122.084)

# Roles
eng_mgr_role = Role.objects.create(title="Engineering Manager", department=eng)
swe_role = Role.objects.create(title="Software Engineer", department=eng)
backend_role = Role.objects.create(title="Backend Developer", department=eng)

design_mgr_role = Role.objects.create(title="Design Manager", department=design)
uiux_role = Role.objects.create(title="UI/UX Designer", department=design)
prod_design_role = Role.objects.create(title="Product Designer", department=design)

# Users
manager_user = User.objects.create_user(username="evan", email="evan@nurux.com", password="password", first_name="Evan", last_name="Manager", role="hr_officer")
emp1_user = User.objects.create_user(username="sarah", email="sarah@nurux.com", password="password", first_name="Sarah", last_name="Johnson", role="employee")
emp2_user = User.objects.create_user(username="michael", email="michael@nurux.com", password="password", first_name="Michael", last_name="James", role="employee")
emp3_user = User.objects.create_user(username="david", email="david@nurux.com", password="password", first_name="David", last_name="Okoro", role="employee")
emp4_user = User.objects.create_user(username="grace", email="grace@nurux.com", password="password", first_name="Grace", last_name="Williams", role="employee")

# Employees
Employee.objects.create(user=manager_user, first_name="Evan", last_name="Manager", department=eng, role=eng_mgr_role)
emp1 = Employee.objects.create(user=emp1_user, first_name="Sarah", last_name="Johnson", department=eng, role=swe_role)
emp2 = Employee.objects.create(user=emp2_user, first_name="Michael", last_name="James", department=design, role=uiux_role)
emp3 = Employee.objects.create(user=emp3_user, first_name="David", last_name="Okoro", department=eng, role=backend_role)
emp4 = Employee.objects.create(user=emp4_user, first_name="Grace", last_name="Williams", department=design, role=prod_design_role)

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
