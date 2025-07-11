from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from .models import ExhibitionTier, ExhibitionOption, ExhibitionImage
from .serializers import ExhibitionTierSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ExhibitionListAPIView(APIView):
    """
    API endpoint to retrieve exhibition tiers and their associated options and images.
    Supports filtering by tier name.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tier_name = request.data.get('tier', None)
        # Prefetch related options and images to minimize database queries
        queryset = ExhibitionTier.objects.prefetch_related(
            Prefetch(
                'options',
                queryset=ExhibitionOption.objects.prefetch_related('images').order_by('type', 'stand_size')
            )
        )

        if tier_name:
            queryset = queryset.filter(name__iexact=tier_name) # Case-insensitive filter

        serializer = ExhibitionTierSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)