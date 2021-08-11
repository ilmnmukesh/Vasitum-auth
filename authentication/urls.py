from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.RegisterView, name="register"),
    path('register/google/', views.GoogleRegisterView, name="google_register"),
    path('login/', views.LoginView, name="login"),
    path('login/google/', views.GoogleLoginView, name="google_login"),
    path("resend/otp/", views.ResendOTP, name="resend_otp"),
]