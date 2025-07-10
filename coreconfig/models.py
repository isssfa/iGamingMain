from django.db import models

class EnvironmentSetting(models.Model):
    SETTING_TYPE_CHOICES = [
        ('ALLOWED_HOST', 'Allowed Host'),
        ('CORS_ORIGIN', 'CORS Allowed Origin'),
        ('CSRF_TRUSTED_ORIGIN', 'CSRF Trusted Origin'),
    ]

    setting_type = models.CharField(max_length=32, choices=SETTING_TYPE_CHOICES)
    value = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return f"{self.get_setting_type_display()}: {self.value}"
