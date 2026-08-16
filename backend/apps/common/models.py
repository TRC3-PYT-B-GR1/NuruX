from django.db import models

class AppVersion(models.Model):
    version_code = models.IntegerField(help_text="Android version code (e.g., 2)")
    version_name = models.CharField(max_length=50, help_text="Version string (e.g., '1.0.1')")
    release_notes = models.TextField(blank=True)
    apk_file = models.FileField(
        upload_to='apks/',
        blank=True,
        null=True,
        help_text="Optional local APK upload. Use download_url for ephemeral hosting platforms.",
    )
    download_url = models.URLField(
        blank=True,
        help_text="Durable external URL, such as a GitHub Release asset.",
    )
    is_mandatory = models.BooleanField(default=False, help_text="Force users to update immediately")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version_code']

    def __str__(self):
        return f"Version {self.version_name} ({self.version_code})"
