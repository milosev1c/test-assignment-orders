from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth', TokenObtainPairView.as_view(), name="token_authorization"),
        path('refresh', TokenRefreshView.as_view(), name="token_refresh")
    ]))
]
