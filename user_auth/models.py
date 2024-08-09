import datetime
import uuid
from django.db import models

from django.contrib.auth.models import AbstractUser, PermissionsMixin

from user_auth.managers import UserManager
from user_auth.common.constants import (
    SocialType, DeviceType
)


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_seconds_since_creation(self):
        return (datetime.datetime.utcnow() - self.created_at.replace(tzinfo=None)).seconds


class User(BaseModel, AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    mobile = models.CharField(max_length=12)
    password = models.CharField(max_length=500, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    profile_image = models.URLField(null=True)
    social_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    social_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=[(tag.name, tag.value) for tag in SocialType]
    )
    social_login = models.BooleanField(default=False)
    device_token = models.CharField(max_length=500, null=True, blank=True)
    device_type = models.CharField(
        max_length=10,
        choices=[(tag.name, tag.value) for tag in DeviceType],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.email

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'User'


class EmailVerification(BaseModel):
    email = models.EmailField(max_length=150, null=True, blank=True)
    otp = models.IntegerField()
    is_used = models.BooleanField(default=False)
    expiry_timestamp = models.DateTimeField(null=True, blank=True)
