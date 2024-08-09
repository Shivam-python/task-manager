from task_management.utils.enum_utility import BaseEnum


class SocialType(BaseEnum):
    FACEBOOK = 'facebook'
    GOOGLE = 'google'
    WHATSAPP = 'whatsapp'
    APPLE = 'apple'


class DeviceType(BaseEnum):
    ANDROID = 'android'
    IOS = 'ios'
    WEB = 'web'


EMAIL_VERIFICATION_SUBJECT = "Code for Email Setup"

