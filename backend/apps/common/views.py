import logging
from datetime import date

from django.conf import settings
from django.db import connection
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.common.permissions import IsManagerOrHR
from apps.employees.models import Employee
from attendance.models import Attendance
from leave.models import LeaveRequest
from payroll.models import PayrollRun
from .models import AppVersion
from .serializers import AppVersionSerializer

logger = logging.getLogger(__name__)


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        try:
            connection.ensure_connection()
        except Exception:
            logger.exception('Database health check failed')
            return Response({'status': 'unhealthy'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'status': 'ok'})


class LatestAppVersionView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        latest_version = AppVersion.objects.first()
        if latest_version:
            return Response(AppVersionSerializer(latest_version, context={'request': request}).data)
        return Response({'detail': 'No versions found.'}, status=status.HTTP_404_NOT_FOUND)


class AIBaseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManagerOrHR]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'ai'

    def generate(self, prompt):
        if not settings.GEMINI_API_KEY:
            return None
        from google import genai

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text

    def hr_context(self):
        """Build a small, permission-safe snapshot for the presentation assistant."""
        try:
            employees = Employee.objects.filter(status='active')
            today = date.today()
            today_attendance = Attendance.objects.filter(date=today)
            pending_leave = LeaveRequest.objects.filter(status=LeaveRequest.Status.PENDING).count()
            return {
                'active_staff': employees.count(),
                'departments': employees.values('department_id').distinct().count(),
                'clocked_in_today': today_attendance.filter(clock_in__isnull=False).count(),
                'late_today': today_attendance.filter(status=Attendance.Status.LATE).count(),
                'pending_leave_requests': pending_leave,
                'payroll_runs': PayrollRun.objects.count(),
            }
        except Exception:
            logger.exception('Could not build AI HR context')
            return {}


class AIChatView(AIBaseView):
    def post(self, request):
        query = str(request.data.get('query', '')).strip()
        if not query:
            return Response({'error': 'Query is required.'}, status=400)
        if len(query) > 2000:
            return Response({'error': 'Query must be 2,000 characters or fewer.'}, status=400)

        try:
            context = self.hr_context()
            answer = self.generate(
                'You are NuruX AI, an HR operations assistant. Answer concisely and clearly. '
                'Use the supplied aggregate metrics only; never reveal personal employee data. '
                f'Aggregate metrics: {context}. Question: {query}'
            )
            if answer is None:
                # Keep the demo useful even when Gemini is not configured on the server.
                lowered = query.lower()
                if 'attendance' in lowered or 'late' in lowered:
                    answer = (f"Today, {context.get('clocked_in_today', 0)} staff have clocked in and "
                              f"{context.get('late_today', 0)} late attendance flag(s) were recorded.")
                elif 'leave' in lowered:
                    answer = f"There are {context.get('pending_leave_requests', 0)} leave request(s) awaiting approval."
                elif 'payroll' in lowered:
                    answer = f"The system has {context.get('payroll_runs', 0)} payroll run(s) recorded."
                else:
                    answer = (f"NuruX is tracking {context.get('active_staff', 0)} active staff across "
                              f"{context.get('departments', 0)} department(s). Ask me about attendance, leave, or payroll.")
            return Response({'response': answer})
        except Exception:
            logger.exception('AI query failed')
            return Response({'error': 'AI service is temporarily unavailable.'}, status=502)


class AIInsightsView(AIBaseView):
    def get(self, request):
        try:
            context = self.hr_context()
            summary = self.generate(
                'Generate a concise two-sentence HR operations insight from these aggregate metrics. '
                f'Metrics: {context}. Do not invent numbers or reveal personal data.'
            )
            if summary is None:
                late = context.get('late_today', 0)
                pending = context.get('pending_leave_requests', 0)
                if late or pending:
                    summary = (f"NuruX has {late} late attendance flag(s) and {pending} pending leave request(s) today. "
                               'Review these items to keep workforce operations moving.')
                else:
                    summary = 'Workforce operations look healthy today. Attendance and leave queues are currently clear.'
            return Response({'summary': summary})
        except Exception:
            logger.exception('AI insight generation failed')
            return Response({'error': 'AI service is temporarily unavailable.'}, status=502)
