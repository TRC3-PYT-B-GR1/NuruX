from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create or update a Super Admin user with role='super_admin'"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, default="admin", help="Admin username (default: admin)")
        parser.add_argument("--email", type=str, default="admin@nurux.com", help="Admin email")
        parser.add_argument("--password", type=str, help="Admin password (if omitted, will prompt)")

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]

        if not password:
            import getpass
            password = getpass.getpass("Enter Super Admin password: ")
            confirm = getpass.getpass("Confirm password: ")
            if password != confirm:
                self.stderr.write(self.style.ERROR("Passwords do not match."))
                return

        user, created = User.objects.get_or_create(username=username, defaults={"email": email})
        user.email = email
        user.set_password(password)
        user.role = User.Role.SUPER_ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"Successfully {action.lower()} Super Admin user '{username}' ({email}) with role 'super_admin'."))
