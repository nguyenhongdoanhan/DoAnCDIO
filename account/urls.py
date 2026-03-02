from django.urls import path, include
from . import views

urlpatterns = [

    # HTML
    path("signup/", views.signup_page, name="signup"),
    path("", include("tts.urls")),
    path("library/", views.library_view, name="library"),
    path("clone/", views.clone_view, name="clone"),
    path("pricing/", views.pricing_view, name="pricing"),
    path("update-plan/", views.update_plan, name="update-plan"),

    # API AUTH
    path("api/auth/", views.auth, name="api-auth"),
]