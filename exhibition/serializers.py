from rest_framework import serializers
from .models import ExhibitionTier, ExhibitionOption, ExhibitionImage
import base64
import mimetypes

class ExhibitionImageBase64Field(serializers.SerializerMethodField):
    """
    Custom SerializerMethodField to return the Base64 image with Data URI prefix.
    """
    def to_representation(self, obj):
        if obj.image and obj.image.path:
            try:
                with open(obj.image.path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

                mime_type, _ = mimetypes.guess_type(obj.image.path)
                if mime_type is None:
                    mime_type = 'application/octet-stream' # Default if type cannot be guessed

                return f"data:{mime_type};base64,{encoded_string}"
            except FileNotFoundError:
                return None
            except Exception as e:
                print(f"Error processing image {obj.image.path}: {e}")
                return None
        return None


class ExhibitionOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for ExhibitionOption, customizing benefit and note fields to lists,
    and including a flat list of Base64 images.
    """
    standSize = serializers.CharField(source='stand_size')
    standBenefits = serializers.SerializerMethodField()
    exhibitorBenefits = serializers.SerializerMethodField()
    sponsorshipStatus = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()

    # Changed: Now images will be a list of base64 strings directly
    images = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, localize=True)

    class Meta:
        model = ExhibitionOption
        fields = [
            'type',
            'standSize',
            'price',
            'description',
            'standBenefits',
            'exhibitorBenefits',
            'sponsorshipStatus',
            'notes',
            'images',
        ]

    def _split_text_field(self, text):
        if text:
            if '\n' in text:
                return [item.strip() for item in text.split('\n') if item.strip()]
            else:
                return [item.strip() for item in text.split(',') if item.strip()]
        return []

    def get_standBenefits(self, obj):
        return self._split_text_field(obj.stand_benefits)

    def get_exhibitorBenefits(self, obj):
        return self._split_text_field(obj.exhibitor_benefits)

    def get_sponsorshipStatus(self, obj):
        return self._split_text_field(obj.sponsorship_status)

    def get_notes(self, obj):
        return self._split_text_field(obj.notes)

    def get_images(self, obj):
        """
        Returns a list of Base64 image strings for the related images.
        """
        image_list = []
        for img_obj in obj.images.all():
            base64_data = ExhibitionImageBase64Field().to_representation(img_obj)
            if base64_data:
                image_list.append(base64_data)
        return image_list


class ExhibitionTierSerializer(serializers.ModelSerializer):
    """
    Serializer for ExhibitionTier, nesting ExhibitionOptionSerializer to include options.
    """
    tier = serializers.CharField(source='name')
    options = ExhibitionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ExhibitionTier
        fields = ['tier', 'options']