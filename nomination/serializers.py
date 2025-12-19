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
            'company',
            'role',
            'nominated_company',
            'award_category',
            'reason_for_nomination',
        ]
    
    def to_internal_value(self, data):
        # Map camelCase to snake_case for API compatibility
        camel_to_snake = {
            'fullName': 'full_name',
            'phoneNumber': 'phone_number',
            'nominatedCompany': 'nominated_company',
            'awardCategory': 'award_category',
            'reasonForNomination': 'reason_for_nomination',
        }
        
        # Convert camelCase keys to snake_case
        converted_data = {}
        for key, value in data.items():
            snake_key = camel_to_snake.get(key, key)
            converted_data[snake_key] = value
        
        return super().to_internal_value(converted_data)

