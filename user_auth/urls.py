from django.urls import path
from user_auth.views import UserSignup, UserVerification

urlpatterns = [
    path('sign-up', UserSignup.as_view()),
    path('verify-otp', UserVerification.as_view()),
]
