from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="JobPosting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("department", models.CharField(blank=True, max_length=100)),
                ("status", models.CharField(choices=[("open", "Open"), ("closed", "Closed")], default="open", max_length=10)),
                ("date_posted", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="job_postings", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-date_posted"]},
        ),
        migrations.CreateModel(
            name="Candidate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=200)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("stage", models.CharField(choices=[("applied", "Applied"), ("screening", "Screening"), ("interview", "Interview"), ("offer", "Offer"), ("rejected", "Rejected"), ("hired", "Hired")], default="applied", max_length=20)),
                ("score", models.PositiveSmallIntegerField(default=0)),
                ("applied_at", models.DateTimeField(auto_now_add=True)),
                ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="candidates", to="recruitment.jobposting")),
            ],
            options={"ordering": ["-applied_at"]},
        ),
    ]
