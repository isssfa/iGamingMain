from django.db import models
from django.contrib.auth.models import User


class Nomination(models.Model):
    """
    Model for award nominations.
    Captures information about the nominator and the nominated company.
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    nominated_company = models.CharField(max_length=255)
    award_category = models.CharField(max_length=255)
    reason_for_nomination = models.TextField()
    
    # Status and audit fields
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.nominated_company} ({self.award_category})"

