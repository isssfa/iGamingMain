from django.urls import path, include

urlpatterns = [
    path('base/', include('base.urls')),
    path('sponsor/', include('sponsor.urls')),
    path('sponsorship/', include('sponsorship.urls')),
    path('exhibition/', include('exhibition.urls')),
    path('speakers/', include('speakers.urls')),
]