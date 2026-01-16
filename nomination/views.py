from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Nomination
from .serializers import NominationSerializer
from logs.utils import log_message
from security.permissions import ProtectedPostPermission


class NominationView(APIView):
    """
    API endpoint to accept award nomination submissions.
    Sends email notification upon successful submission.
    """
    permission_classes = [ProtectedPostPermission]
    rate_limit = '10/m'  # 10 requests per minute

    def post(self, request):
        serializer = NominationSerializer(data=request.data)
        if serializer.is_valid():
            nomination = serializer.save()
            
            # Email logic
            email_sent = False
            try:
                context = {
                    "full_name": nomination.full_name or "Not provided",
                    "email": nomination.email or "Not provided",
                    "phone_number": nomination.phone_number or "Not provided",
                    "company": nomination.company or "Not provided",
                    "role": nomination.role or "Not provided",
                    "nominated_company": nomination.nominated_company or "Not provided",
                    "award_category": nomination.award_category or "Not provided",
                    "background_information": nomination.background_information or "Not provided",
                    "specific_instance_project": nomination.specific_instance_project or "Not provided",
                    "impact_on_industry": nomination.impact_on_industry or "Not provided",
                    "created_at": nomination.created_at,
                }
                message = render_to_string('nomination/email/nomination_notification.html', context)
                email = EmailMessage(
                    subject=f"🏆 New Award Nomination - {nomination.nominated_company}",
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.NOTIFICATION_EMAIL]
                )
                email.content_subtype = 'html'
                email.send()
                email_sent = True
            except Exception as e:
                user = getattr(request, 'user', None) if hasattr(request, 'user') and request.user.is_authenticated else None
                log_message("ERROR", f"Nomination email send failed: {e}", user=user,
                            source_app='nomination_NominationView_1')

            nomination.email_sent = email_sent
            nomination.save(update_fields=['email_sent'])

            user = getattr(request, 'user', None) if hasattr(request, 'user') and request.user.is_authenticated else None
            log_message("INFO", f"Nomination received from {nomination.full_name} for {nomination.nominated_company}", 
                       user=user, source_app='nomination_NominationView_2')
            
            return Response(
                {"message": "Nomination submitted successfully."}, 
                status=status.HTTP_201_CREATED
            )

        user = getattr(request, 'user', None) if hasattr(request, 'user') and request.user.is_authenticated else None
        log_message("CRITICAL", f"Nomination validation failed: {serializer.errors}", 
                   user=user, source_app='nomination_NominationView_3')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

