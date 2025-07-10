from django.db import models
from django.contrib.auth.models import User
import os
import time
from django.utils.text import slugify

class PackageBenefitItem(models.Model):
    item = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return self.item

class PlatinumItem(models.Model):
    item = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return self.item

class SilverItem(models.Model):
    item = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return self.item

class GoldItem(models.Model):
    item = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return self.item

class ImportantNoteItem(models.Model):
    item = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return self.item[:50]


def sponsorship_icon_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    timestamp = int(time.time())
    sponsor_slug = slugify(instance.name)
    filename = f"{sponsor_slug}_{timestamp}.{ext}"
    return os.path.join('sponsorship', filename)


class Sponsorship(models.Model):
    STATUS_TYPES = [
        ('on_hold', 'On Hold'),
        ('available', 'Available'),
        ('taken', 'Taken'),
    ]
    name = models.CharField(max_length=255)
    package_benefit = models.BooleanField(default=False)
    package_items = models.ManyToManyField(PackageBenefitItem, related_name='package_benefit_items', blank=True)
    platinum_status = models.BooleanField("Platinum Sponsorship Status", default=False)
    platinum_items = models.ManyToManyField(PlatinumItem, related_name='platinum_items', blank=True)
    gold_status = models.BooleanField("Gold Sponsorship Status", default=False)
    gold_items = models.ManyToManyField(GoldItem, related_name='gold_items', blank=True)
    silver_status = models.BooleanField("Silver Sponsorship Status", default=False)
    silver_items = models.ManyToManyField(SilverItem, related_name='silver_items', blank=True)
    important_notes = models.BooleanField(default=False)
    important_items = models.ManyToManyField(ImportantNoteItem, related_name='important_notes_items', blank=True)
    included_tickets = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to=sponsorship_icon_upload_path, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_TYPES, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return self.name
