from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Speaker
from .serializers import SpeakerSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class SpeakerViewSet(APIView):
    """
    API endpoint to retrieve exhibition tiers and their associated options and images.
    Supports filtering by tier name.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        company = request.data.get('company', None)
        role = request.data.get('role', None)

        # Prefetch related options and images to minimize database queries
        queryset = Speaker.objects.all()

        if name:
            queryset = queryset.filter(name__iexact=name)
        if company:
            queryset = queryset.filter(company__iexact=company)
        if role:
            queryset = queryset.filter(role__iexact=role)

        serializer = SpeakerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)