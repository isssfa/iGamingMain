from rest_framework import serializers
from .models import Sponsor
import base64
import imghdr
import uuid
from django.core.files.base import ContentFile


class SponsorSerializer(serializers.ModelSerializer):
    logo_base64 = serializers.SerializerMethodField()
    added_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Sponsor
        fields = [
            'id',
            'name',
            'logo_base64',
            'type',
            'created_at',
            'updated_at',
            'added_by',
        ]

    def get_logo_base64(self, obj):
        if obj.logo:
            try:
                with obj.logo.open('rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    file_type = obj.logo.name.split('.')[-1]
                    return f"data:image/{file_type};base64,{encoded_string}"
            except Exception as e:
                return None
        return None
