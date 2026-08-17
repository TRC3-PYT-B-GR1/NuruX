import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("employees", "0002_employee_department_employee_role")]
    operations = [
        migrations.AddField("employee", "phone", models.CharField(blank=True, max_length=30)),
        migrations.AddField("employee", "address", models.TextField(blank=True)),
        migrations.AddField("employee", "date_of_birth", models.DateField(blank=True, null=True)),
        migrations.AddField("employee", "gender", models.CharField(blank=True, max_length=30)),
        migrations.AddField("employee", "nationality", models.CharField(blank=True, max_length=80)),
        migrations.AddField("employee", "identification_number", models.CharField(blank=True, max_length=100)),
        migrations.AddField("employee", "employment_type", models.CharField(choices=[("full_time", "Full time"), ("part_time", "Part time"), ("contract", "Contract"), ("temporary", "Temporary"), ("intern", "Intern")], default="full_time", max_length=20)),
        migrations.AddField("employee", "salary_grade", models.CharField(blank=True, max_length=50)),
        migrations.AddField("employee", "exit_date", models.DateField(blank=True, null=True)),
        migrations.AddField("employee", "exit_reason", models.TextField(blank=True)),
        migrations.AddField("employee", "next_of_kin_name", models.CharField(blank=True, max_length=160)),
        migrations.AddField("employee", "next_of_kin_relationship", models.CharField(blank=True, max_length=80)),
        migrations.AddField("employee", "next_of_kin_phone", models.CharField(blank=True, max_length=30)),
        migrations.AddField("employee", "next_of_kin_address", models.TextField(blank=True)),
        migrations.AddField("employee", "emergency_contact_name", models.CharField(blank=True, max_length=160)),
        migrations.AddField("employee", "emergency_contact_relationship", models.CharField(blank=True, max_length=80)),
        migrations.AddField("employee", "emergency_contact_phone", models.CharField(blank=True, max_length=30)),
        migrations.AddField("employee", "emergency_contact_address", models.TextField(blank=True)),
        migrations.AddField("employee", "manager", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="direct_reports", to="employees.employee")),
        migrations.CreateModel(
            name="EmploymentHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employer", models.CharField(max_length=200)), ("job_title", models.CharField(max_length=160)),
                ("start_date", models.DateField(blank=True, null=True)), ("end_date", models.DateField(blank=True, null=True)), ("notes", models.TextField(blank=True)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="employment_history", to="employees.employee")),
            ], options={"ordering": ["-start_date", "-id"]},
        ),
        migrations.CreateModel(
            name="EducationRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("institution", models.CharField(max_length=200)), ("qualification", models.CharField(max_length=160)), ("field_of_study", models.CharField(blank=True, max_length=160)),
                ("start_date", models.DateField(blank=True, null=True)), ("end_date", models.DateField(blank=True, null=True)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="education_records", to="employees.employee")),
            ], options={"ordering": ["-end_date", "-id"]},
        ),
        migrations.CreateModel(
            name="Certification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)), ("issuer", models.CharField(blank=True, max_length=180)), ("issue_date", models.DateField(blank=True, null=True)), ("expiry_date", models.DateField(blank=True, null=True)), ("credential_id", models.CharField(blank=True, max_length=120)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="certifications", to="employees.employee")),
            ], options={"ordering": ["-issue_date", "-id"]},
        ),
        migrations.CreateModel(
            name="EmployeeSkill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=120)), ("proficiency", models.CharField(blank=True, max_length=30)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="skills", to="employees.employee")),
            ], options={"ordering": ["name"], "constraints": [models.UniqueConstraint(fields=("employee", "name"), name="unique_employee_skill")]},
        ),
        migrations.CreateModel(
            name="PromotionHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("previous_role", models.CharField(blank=True, max_length=160)), ("new_role", models.CharField(max_length=160)), ("effective_date", models.DateField()), ("notes", models.TextField(blank=True)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="promotion_history", to="employees.employee")),
            ], options={"ordering": ["-effective_date", "-id"]},
        ),
    ]
