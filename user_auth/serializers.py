import re
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from user_auth.common import messages as app_messages
from user_auth.models import (
    User,
    EmailVerification
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_email(self, value: str) -> str:
        """
        A function to validate email
        """
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError(app_messages.INVALID_EMAIL_FORMAT)
        return value

    def validate_mobile(self, value: str) -> str:
        """
        A function to validate Indian mobile number
        """
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError(app_messages.INVALID_MOBILE_NUMBER)
        return value

    def validate_password(self, str) -> str:
        """
        A function to save the password for storing the values
        """
        return make_password(str)


class UserVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate_email(self, value: str) -> str:
        """
        A function to validate email
        """
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError(app_messages.INVALID_EMAIL_FORMAT)

        return value

    def validate_otp(self, value: str) -> str:
        """
        A function to validate otp
        """
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError(app_messages.INVALID_OTP)

        return value

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        evf_obj = EmailVerification.objects.filter(email=email, otp=otp, is_used=False).order_by('-created_at').first()

        if not evf_obj:
            raise serializers.ValidationError(app_messages.INCORRECT_OTP)

        if evf_obj.expiry_timestamp.replace(tzinfo=None) < datetime.now():
            raise serializers.ValidationError(app_messages.EXPIRED_OTP)

        return data
