"""Configuration racine des routes du projet LITRevu.

Les routes propres à chaque fonctionnalité sont déléguées aux applications
``authentication`` et ``reviews``.
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # La racine du site conduit un visiteur vers l'écran de connexion.
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('reviews.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
