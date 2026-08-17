from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_new_password(self, value):
        validate_password(value, user=self.context['request'].user)
        return value


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
        username_or_email = str(attrs.get("username", "")).strip()
        attrs["username"] = username_or_email

        # Allow login via email by mapping it to the username
        if "@" in username_or_email:
            user_by_email = User.objects.filter(email__iexact=username_or_email).first()
            if user_by_email:
                attrs["username"] = user_by_email.username
                username = user_by_email.username
            else:
                username = username_or_email
        else:
            username = username_or_email

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

        data["user"] = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        }
        return data
