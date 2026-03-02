from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    update_plan,
    login_page,
    dashboard_page,
    logout_view,
    subtitle_page,
    subtitle_convert,
    tasks_page,
    projects_page,
    library_page,
    clone_page,
    pricing_page,
    settings_page,
)

urlpatterns = [

    # ================= ADMIN =================
    path("admin/", admin.site.urls),

    # ================= HTML =================
    path("", login_page, name="login"),
    path("dashboard/", dashboard_page, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path("subtitle/", subtitle_page, name="subtitle"),
    path("tasks/", tasks_page, name="tasks"),
    path("projects/", projects_page, name="projects"),
    path("library/", library_page, name="library"),
    path("clone/", clone_page, name="clone"),
    path("pricing/", pricing_page, name="pricing"),
    path("update-plan/", update_plan, name="update_plan"),
    path("settings/", settings_page, name="settings"),

    # ================= SUBTITLE API =================
    path("subtitle/convert/", subtitle_convert, name="subtitle_convert"),

    # ================= ACCOUNT =================
    path("", include("account.urls")),

    # ================= JWT =================
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # ================= TTS =================
    path("api/", include("tts.urls")),

    # ================= PASSWORD RESET =================
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="UI/password_reset.html",
            success_url=reverse_lazy("password_reset_done")
        ),
        name="password_reset"
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="UI/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="UI/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete")
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="UI/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)