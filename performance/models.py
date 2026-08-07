from django.db import models


class KPI(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    target = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Goal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    target_date = models.DateField()

    status_choices = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PerformanceReview(models.Model):
    employee_name = models.CharField(max_length=100)
    reviewer_name = models.CharField(max_length=100)

    rating = models.IntegerField()

    comments = models.TextField()

    review_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} Review"
    
class ManagerFeedback(models.Model):
    employee_name = models.CharField(max_length=100)
    manager_name = models.CharField(max_length=100)

    feedback = models.TextField()

    feedback_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.manager_name} feedback for {self.employee_name}"