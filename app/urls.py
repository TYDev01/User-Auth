from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("register/", views.signup_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("forgot/", views.forgot_password_view, name="forgot"),
    path("password-reset-sent/<str:reset_id>/", views.password_reset_sent, name="password-reset-sent"),
    path("reset-password/<str:reset_id>/", views.password_reset, name="reset-password")
]
