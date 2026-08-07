from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),

    # ✅ JWT LOGIN (THIS IS THE FIX)
    path('accounts/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('accounts/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include('profiles.urls')),
    path('', include('jobs.urls')),

    path(
    "applications/",
    include("applications.urls")),

    path(
    "api/admin/",
    include("admin_panel.urls")),

    path("payments/", include("payments.urls")),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )