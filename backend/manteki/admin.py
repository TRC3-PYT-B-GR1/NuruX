from django.contrib import admin
from .models import Interview
from django.contrib import admin
from .models import JobPosting, Applicant, Application

# Register your models here.
admin.site.register(JobPosting)
admin.site.register(Applicant)
admin.site.register(Application)
admin.site.register(Interview)