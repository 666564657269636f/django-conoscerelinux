from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    path("my-profile", views.my_profile, name="my-profile"),
    path("verify-email/<int:user_pk>/", views.verify_email, name="verify-email"),
    path("verify-email/done/", views.verify_email_done, name="verify-email-done"),
    path(
        "verify-email-confirm/<uidb64>/<token>/",
        views.verify_email_confirm,
        name="verify-email-confirm",
    ),
    path(
        "verify-email/complete/",
        views.verify_email_complete,
        name="verify-email-complete",
    ),
]
