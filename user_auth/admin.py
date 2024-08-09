from django.contrib import admin
from django import forms
from django.utils.timezone import localtime, timedelta

from user_auth.models import User, EmailVerification

# Register your models here.


class EmailVerificationAdminForm(forms.ModelForm):
    class Meta:
        model = EmailVerification
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.expiry_timestamp:
            # Convert UTC time to IST by subtracting 5 hours and 30 minutes
            ist_time = localtime(self.instance.expiry_timestamp) + timedelta(hours=5, minutes=30)
            self.fields['expiry_timestamp'].initial = ist_time

    def clean_expiry_time(self):
        expiry_timestamp = self.cleaned_data['expiry_timestamp']
        # Convert IST back to UTC by adding 5 hours and 30 minutes
        return expiry_timestamp - timedelta(hours=5, minutes=30)


admin.site.register(User)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    form = EmailVerificationAdminForm
    list_display = ('email', 'otp', 'is_used', 'expiry_timestamp')
    fields = ('email', 'otp', 'is_used', 'expiry_timestamp')