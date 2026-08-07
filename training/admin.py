from django.contrib import admin
from .models import (
    Course,
    Assessment,
    Certificate
)


admin.site.register(Course)
admin.site.register(Assessment)
admin.site.register(Certificate)