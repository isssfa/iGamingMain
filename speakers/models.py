from django.db import models
from django.contrib.auth.models import User
import os
import time
from django.utils.text import slugify


def speaker_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    timestamp = int(time.time())
    sponsor_slug = slugify(instance.name)
    filename = f"{sponsor_slug}_{timestamp}.{ext}"
    return os.path.join('speakers', filename)


class Speaker(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=speaker_image_upload_path, null=True, blank=True)

    # Social Links
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Comma-separated events field
    events = models.TextField(
        help_text="Comma-separated list of events",
        null=True,
        blank=True
    )

    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='speakers_added'
    )

    def __str__(self):
        return self.name

    def get_event_list(self):
        """Returns the events as a list"""
        return [event.strip() for event in self.events.split(",")] if self.events else []
