from rest_framework import serializers
from .models import AppVersion

class AppVersionSerializer(serializers.ModelSerializer):
    apk_url = serializers.SerializerMethodField()

    class Meta:
        model = AppVersion
        fields = [
            'version_code', 'version_name', 'release_notes', 'apk_file',
            'download_url', 'apk_url', 'is_mandatory', 'created_at',
        ]

    def get_apk_url(self, obj):
        if obj.download_url:
            return obj.download_url
        if not obj.apk_file:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(obj.apk_file.url) if request else obj.apk_file.url

    def validate(self, attrs):
        apk_file = attrs.get('apk_file', getattr(self.instance, 'apk_file', None))
        download_url = attrs.get('download_url', getattr(self.instance, 'download_url', ''))
        if not apk_file and not download_url:
            raise serializers.ValidationError('Provide either an APK file or a durable download URL.')
        return attrs
