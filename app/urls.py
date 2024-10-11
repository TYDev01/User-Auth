from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("register/", views.signup_view, name="register"),
    path("login/", views.login_view, name="login")
]
