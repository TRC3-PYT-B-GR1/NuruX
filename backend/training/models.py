from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    instructor = models.CharField(max_length=100)

    duration = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Assessment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assessments'
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    passing_score = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Certificate(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='certificates'
    )

    employee_name = models.CharField(max_length=100)

    certificate_name = models.CharField(max_length=200)

    issue_date = models.DateField()

    certificate_number = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.certificate_name
    
    
