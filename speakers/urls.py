from django.urls import path
from .views import SpeakerViewSet

urlpatterns = [
    path('', SpeakerViewSet.as_view(), name='speaker-list'),
]