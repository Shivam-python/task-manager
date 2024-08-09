from random import randint

from user_auth.helpers.query_helpers.registration import (
    create_user,
    save_email_verification_data,
    update_email_otp_used,
    mark_user_as_verified
)
from user_auth.common import constants, messages as app_messages
from task_management.utils import custom_exceptions as ce
from task_management.utils.response_utils import ResponseHandler


def register_user(validated_data):
    email = validated_data.get("email")

    if send_verification_email(email):
        user = create_user(validated_data)
        return ResponseHandler.success(message=app_messages.USER_REGISTERED, data=dict(email=email))
    else:
        raise ce.EmailVerificationError


def send_verification_email(email):
    try:
        otp = 9999  # str(randint(100000, 999999))
        # send_email(email, constants.EMAIL_VERIFICATION_SUBJECT, otp)
        save_email_verification_data(email, otp)
        return True
    except:
        return False


def verify_user(validated_data):
    try:
        email = validated_data.get("email")
        otp = validated_data.get("otp")
        update_email_otp_used(email=email, otp=otp)
        mark_user_as_verified(email=email)
        return ResponseHandler.success(message=app_messages.USER_VERIFIED)
    except Exception as e:
        return ResponseHandler.failure(message=app_messages.USER_VERIFICATION_FAILED.format(str(e)))
