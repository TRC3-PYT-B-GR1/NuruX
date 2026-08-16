import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ChangePasswordSerializer, LockoutAwareTokenObtainPairSerializer

User = get_user_model()
logger = logging.getLogger(__name__)
reset_token_generator = PasswordResetTokenGenerator()


class LoginView(TokenObtainPairView):
    """POST {username, password} -> {access, refresh}"""

    serializer_class = LockoutAwareTokenObtainPairSerializer


class LogoutView(APIView):
    """
    POST {refresh} -> 205
    Blacklists the refresh token so it can no longer be used to mint new
    access tokens (requires the token_blacklist app, already installed).
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid or already-expired token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class MeView(APIView):
    """GET current authenticated user's identity + role — used by the frontend to gate UI."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
            }
        )


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data['current_password']):
            return Response(
                {'current_password': ['Current password is incorrect.']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])
        return Response({'detail': 'Password changed successfully.'})


class PasswordResetRequestView(APIView):
    """POST {email} -> 200 always (never reveal whether the email exists)."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip()
        user = User.objects.filter(email__iexact=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = reset_token_generator.make_token(user)
            reset_url = f"https://nurux.duckdns.org/reset-password/{uid}/{token}/"
            logger.info("Password reset link for %s: %s", user.email, reset_url)
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                send_mail(
                    subject="NuruX Password Reset",
                    message=(
                        f"Hello {user.first_name or user.username},\n\n"
                        f"A password reset was requested for your NuruX account.\n\n"
                        f"Click the link below to reset your password:\n{reset_url}\n\n"
                        "If you did not request this, please ignore this email."
                    ),
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None) or None,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception:
                logger.exception("Failed to send password reset email to %s", user.email)
        return Response({"detail": "If that email exists, a reset link has been sent."})


class PasswordResetConfirmView(APIView):
    """POST {uid, token, new_password} -> 200 / 400"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not all([uid, token, new_password]):
            return Response({"detail": "uid, token, and new_password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"detail": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        if not reset_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired reset link."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as exc:
            return Response({'new_password': list(exc.messages)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.register_successful_login()  # also clears any lockout
        user.save()
        return Response({"detail": "Password has been reset successfully."})
