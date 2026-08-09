from django.contrib import admin
from .models import KPI, Goal, PerformanceReview, ManagerFeedback  

admin.site.register(KPI)
admin.site.register(Goal)
admin.site.register(PerformanceReview)
admin.site.register(ManagerFeedback)
