from rest_framework import serializers
from .models import Sponsorship

class SponsorshipSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sponsorship model, formatting benefits as lists
    and providing the full URL for icon_image.
    """
    # Use SerializerMethodField for benefit fields to split them into lists
    benefits = serializers.SerializerMethodField()
    platinumBenefits = serializers.SerializerMethodField()
    diamondBenefits = serializers.SerializerMethodField()
    goldBenefits = serializers.SerializerMethodField()
    silverBenefits = serializers.SerializerMethodField()
    bronzeBenefits = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField() # For notes as well, if it contains multiple items

    # Rename the icon_image field to 'images' as requested in the output
    images = serializers.SerializerMethodField()

    class Meta:
        model = Sponsorship
        fields = [
            'id', 'title', 'price', 'status', 'icon', 'iconBg', 'description',
            'benefits', 'platinumBenefits', 'diamondBenefits', 'goldBenefits', 'silverBenefits',
            'bronzeBenefits', 'notes', 'tickets', 'images'
        ]

    def _split_text_field(self, text):
        """Helper to split comma/newline separated text into a list."""
        if not text:
            return []
        # Split by comma or newline, then strip whitespace from each item
        items = [item.strip() for item in text.replace('\n', ',').split(',') if item.strip()]
        return items

    def get_benefits(self, obj):
        return self._split_text_field(obj.benefits)

    def get_platinumBenefits(self, obj):
        # Note the casing change from model field `platinum_benefits` to output `platinumBenefits`
        return self._split_text_field(obj.platinum_benefits)

    def get_diamondBenefits(self, obj):
        return self._split_text_field(obj.diamond_benefits)

    def get_goldBenefits(self, obj):
        return self._split_text_field(obj.gold_benefits)

    def get_silverBenefits(self, obj):
        return self._split_text_field(obj.silver_benefits)

    def get_bronzeBenefits(self, obj):
        return self._split_text_field(obj.bronze_benefits)

    def get_notes(self, obj):
        return self._split_text_field(obj.notes)

    def get_images(self, obj):
        request = self.context.get('request')  # Only works in serializers with context
        if obj.icon_image and request:
            return request.build_absolute_uri(obj.icon_image.url)
        return None

    # def get_images(self, obj):
    #     if obj.icon_image:
    #         try:
    #             with obj.icon_image.open('rb') as image_file:
    #                 encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    #                 file_type = obj.icon_image.name.split('.')[-1]
    #                 return f"data:image/{file_type};base64,{encoded_string}"
    #         except Exception as e:
    #             return None
    #     return None