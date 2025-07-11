from django.urls import path, include

urlpatterns = [
    path('', include('base.urls')),
    path('sponsors/', include('sponsor.urls')),
    path('sponsorships/', include('sponsorship.urls')),
    path('exhibition/', include('exhibition.urls')),
    path('speakers/', include('speakers.urls')),
]