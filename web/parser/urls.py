from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from parser.views import *

urlpatterns = [
    # ===WEB urls==
    # Main urls.
    path("", index, name="index"),
    path("auth", auth, name="auth"),
    path("profile", profile, name="profile"),
    path("logout", logout_view, name="logout_view"),
    path("run_parse/", run_parse, name="run_parse"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)