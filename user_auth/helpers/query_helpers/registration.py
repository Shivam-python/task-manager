from datetime import datetime, timedelta
from user_auth.models import (
    User,
    EmailVerification
)


def create_user(validated_data):
    user = User.objects.create_user(**validated_data)
    return user


def save_email_verification_data(email, otp):
    expiry_timestamp = datetime.now() + timedelta(seconds=600)
    verification = EmailVerification(
        email=email,
        otp=otp,
        expiry_timestamp=expiry_timestamp
    )
    verification.save()


def update_email_otp_used(email, otp):
    evf_obj = EmailVerification.objects.filter(email=email, otp=otp).first()
    evf_obj.is_used = True
    evf_obj.save()


def mark_user_as_verified(email):
    user = User.objects.get(email=email)
    user.is_verified = True
    user.save()
