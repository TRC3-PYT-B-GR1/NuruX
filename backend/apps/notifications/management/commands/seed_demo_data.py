from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from apps.notifications.models import Notification
from apps.recruitment.models import Candidate, JobPosting


class Command(BaseCommand):
    help = "Create safe presentation data for recruitment and notifications."

    def add_arguments(self, parser):
        parser.add_argument("--username", help="User who should receive the demo notifications")

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get("username")
        user = User.objects.filter(username=username).first() if username else User.objects.order_by("id").first()
        if not user:
            raise CommandError("No user exists. Create a staff user first.")

        jobs = [
            ("Product Designer", "Design", "Own product discovery and design systems."),
            ("Backend Engineer", "Engineering", "Build reliable Django services for workforce operations."),
            ("HR Business Partner", "People", "Partner with leaders on people strategy and performance."),
            ("Data Analyst", "Strategy", "Turn workforce data into clear decisions."),
        ]
        created_jobs = {}
        for title, department, description in jobs:
            job, _ = JobPosting.objects.get_or_create(title=title, defaults={"department": department, "description": description, "created_by": user})
            created_jobs[title] = job

        candidates = [
            ("Amina Yusuf", "Product Designer", "interview", 92),
            ("Chinedu Okafor", "Backend Engineer", "screening", 87),
            ("Fatima Bello", "HR Business Partner", "offer", 95),
            ("David Mensah", "Data Analyst", "applied", 78),
            ("Grace Eze", "Backend Engineer", "screening", 84),
        ]
        for name, job_title, stage, score in candidates:
            Candidate.objects.get_or_create(full_name=name, job=created_jobs[job_title], defaults={"stage": stage, "score": score})

        notifications = [
            ("Leave Request", "A leave request is awaiting your review.", "/leave"),
            ("Attendance Alert", "Attendance anomalies are ready for review.", "/reports"),
            ("Recruitment Update", "Amina Yusuf is ready for an interview.", "/recruitment"),
        ]
        for title, body, path in notifications:
            Notification.objects.get_or_create(recipient=user, title=title, defaults={"body": body, "path": path})

        self.stdout.write(self.style.SUCCESS(f"Demo data ready for {user.username}."))
