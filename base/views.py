from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventRegistrationSerializer, InquirySerializer
from .models import EventRegistration
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail


class EventRegistrationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EventRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            registration = serializer.save()
            registration.user = request.user
            registration.save(update_fields=['user'])

            # Email logic...
            email_sent = False
            try:
                context = {
                    "first_name": registration.first_name,
                    "last_name": registration.last_name,
                    "company_name": registration.company_name,
                    "work_email": registration.work_email,
                    "phone_number": registration.phone_number,
                    "interests": registration.interests,
                    "created_at": registration.created_at,
                }
                message = render_to_string('email/registration_notification.html', context)
                email = EmailMessage(
                    subject=f"📬 New Event Registration Received - {registration.first_name}",
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.NOTIFICATION_EMAIL]
                )
                email.content_subtype = 'html'
                email.send()
                email_sent = True
            except Exception as e:
                print(f"Email send failed: {e}")

            registration.email_sent = email_sent
            registration.save(update_fields=['email_sent'])

            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InquiryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InquirySerializer(data=request.data)
        if serializer.is_valid():
            inquiry = serializer.save()

            # Send email
            try:
                send_mail(
                    subject=f"New Inquiry: {inquiry.topic}",
                    message=f"From: {inquiry.name} <{inquiry.email}>\n\n{inquiry.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.NOTIFICATION_EMAIL],
                    fail_silently=False,
                )
                email_sent = True
            except Exception as e:
                print(f"Inquiry email failed: {e}")

            inquiry.email_sent = email_sent
            inquiry.save(update_fields=['email_sent'])
            return Response({"message": "Inquiry submitted successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
