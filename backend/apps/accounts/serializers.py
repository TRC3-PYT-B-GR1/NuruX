from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class LockoutAwareTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Wraps the standard JWT login to add:
      - account lockout after N consecutive failed attempts (PRD §9)
      - role claim embedded in the token, so the frontend/API can read it
        without an extra round trip
    """

    default_error_messages = {
        "locked": "Account temporarily locked due to repeated failed login attempts. Try again later.",
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["full_name"] = f"{user.first_name} {user.last_name}".strip()
        return token

    def validate(self, attrs):
        username = attrs.get("username")
        user = User.objects.filter(username=username).first()

        if user and user.is_locked:
            raise serializers.ValidationError(
                self.error_messages["locked"], code="locked"
            )

        try:
            data = super().validate(attrs)
        except Exception:
            # Login failed (wrong password / inactive) — count it against the user
            if user:
                user.register_failed_login()
            raise

        # Successful login — reset the counter
        user.register_successful_login()
        return data
