from rest_framework import serializers
from .models import Nomination


class NominationSerializer(serializers.ModelSerializer):
    """
    Serializer for Nomination model submissions.
    Accepts camelCase keys and maps to model fields.
    """
    
    class Meta:
        model = Nomination
        fields = [
            'full_name',
            'email',
            'phone_number',
            'linkedin_url',
            'company',
            'role',
            'nominated_company',
            'award_category',
            'background_information',
            'specific_instance_project',
            'impact_on_industry',
        ]
    
    def to_internal_value(self, data):
        # Map camelCase to snake_case for API compatibility
        camel_to_snake = {
            'fullName': 'full_name',
            'phoneNumber': 'phone_number',
            'linkedinUrl': 'linkedin_url',
            'nominatedCompany': 'nominated_company',
            'awardCategory': 'award_category',
            'backgroundInformation': 'background_information',
            'specificInstanceProject': 'specific_instance_project',
            'impactOnIndustry': 'impact_on_industry',
        }
        
        # Convert camelCase keys to snake_case
        converted_data = {}
        for key, value in data.items():
            snake_key = camel_to_snake.get(key, key)
            converted_data[snake_key] = value
        
        return super().to_internal_value(converted_data)

