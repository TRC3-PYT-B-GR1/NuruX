from django.db import models

# Create your models here.
from django.db import models

class JobPosting(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Applicant(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.full_name} - {self.job.title}" 

class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    interviewer_name = models.CharField(max_length=100)
    scheduled_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    outcome = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Interview for {self.application.applicant.full_name}"    
    
class EmployeeDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('id', 'ID Document'),
        ('contract', 'Contract'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    ]

    employee_reference = models.CharField(max_length=100, help_text="Temporary: employee name/ID until Employee model is linked")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='employee_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_reference} - {self.get_document_type_display()}"
   