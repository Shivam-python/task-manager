# Generated by Django 4.2.13 on 2024-08-09 21:27

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(blank=True, max_length=150, null=True)),
                ('otp', models.IntegerField()),
                ('is_used', models.BooleanField(default=False)),
                ('expiry_timestamp', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(max_length=12)),
                ('password', models.CharField(blank=True, max_length=500, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('profile_image', models.URLField(null=True)),
                ('social_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('social_type', models.CharField(blank=True, choices=[('FACEBOOK', 'facebook'), ('GOOGLE', 'google'), ('WHATSAPP', 'whatsapp'), ('APPLE', 'apple')], max_length=100, null=True)),
                ('social_login', models.BooleanField(default=False)),
                ('device_token', models.CharField(blank=True, max_length=500, null=True)),
                ('device_type', models.CharField(blank=True, choices=[('ANDROID', 'android'), ('IOS', 'ios'), ('WEB', 'web')], max_length=10, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
