from django.db import models
import os
import time
from django.utils.text import slugify
from django.contrib.auth.models import User


def sponsor_logo_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    timestamp = int(time.time())
    sponsor_slug = slugify(instance.name)
    filename = f"{sponsor_slug}_{timestamp}.{ext}"
    return os.path.join('sponsor', filename)


class Sponsor(models.Model):
    SPONSOR_TYPES = [
        ('headline', 'Headline'),
        ('diamond', 'Diamond'),
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('strategic', 'Strategic Partner'),
        ('media', 'Media Partner'),
    ]
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    logo = models.ImageField(upload_to=sponsor_logo_upload_path, null=True, blank=True)
    type = models.CharField(max_length=20, choices=SPONSOR_TYPES, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
