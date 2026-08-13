from django import forms
from .models import Applicant, Application, Interview
from .models import EmployeeDocument

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['full_name', 'email', 'phone']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interviewer_name', 'scheduled_date', 'notes']

class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = ['employee_reference', 'document_type', 'file']        