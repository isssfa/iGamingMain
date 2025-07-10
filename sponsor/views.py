from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SponsorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Sponsor

class SponsorCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sponsors = Sponsor.objects.all().order_by('-created_at')
        serializer = SponsorSerializer(sponsors, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
