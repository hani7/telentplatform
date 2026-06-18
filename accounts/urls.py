from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    AppLoginView, register_role,
    register_player, register_coach, register_agent, register_club,
    verify_otp, resend_otp, logout_view,
)

app_name = "accounts"

urlpatterns = [
    path("login/", AppLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_role, name="register_role"),
    path("register/player/", register_player, name="register_player"),
    path("register/coach/", register_coach, name="register_coach"),
    path("register/agent/", register_agent, name="register_agent"),
    path("register/club/", register_club, name="register_club"),
    path("verify/", verify_otp, name="verify_otp"),
    path("resend-otp/", resend_otp, name="resend_otp"),

    # Password Reset URLs
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset_form.html",
        email_template_name="accounts/password_reset_email.html",
        success_url=reverse_lazy("accounts:password_reset_done")
    ), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        success_url=reverse_lazy("accounts:password_reset_complete")
    ), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ), name="password_reset_complete"),
]

