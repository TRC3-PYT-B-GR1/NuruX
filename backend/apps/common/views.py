import logging

from django.conf import settings
from django.db import connection
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.common.permissions import IsManagerOrHR
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


class AIChatView(AIBaseView):
    def post(self, request):
        query = str(request.data.get('query', '')).strip()
        if not query:
            return Response({'error': 'Query is required.'}, status=400)
        if len(query) > 2000:
            return Response({'error': 'Query must be 2,000 characters or fewer.'}, status=400)

        try:
            answer = self.generate(
                'You are NuruX AI, an HR assistant. Give concise, general HR guidance. '
                'Do not claim access to employee records or reveal private information. '
                f'Question: {query}'
            )
            if answer is None:
                return Response({'error': 'AI service is not configured.'}, status=503)
            return Response({'response': answer})
        except Exception:
            logger.exception('AI query failed')
            return Response({'error': 'AI service is temporarily unavailable.'}, status=502)


class AIInsightsView(AIBaseView):
    def get(self, request):
        try:
            summary = self.generate(
                'Generate a concise two-sentence generic HR operations insight. '
                'Do not invent company metrics or claim access to employee records.'
            )
            if summary is None:
                return Response({'summary': 'AI insights are unavailable until an API key is configured.'})
            return Response({'summary': summary})
        except Exception:
            logger.exception('AI insight generation failed')
            return Response({'error': 'AI service is temporarily unavailable.'}, status=502)
