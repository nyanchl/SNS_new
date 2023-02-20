# Generated by Django 4.1.6 on 2023-02-16 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('username', models.CharField(max_length=30, unique=True, verbose_name='username')),
                ('name', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True, verbose_name='name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('password', models.CharField(max_length=1024, null=True)),
                ('admin', models.BooleanField(default=False, verbose_name='管理サイトアクセス権限')),
                ('last_login', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'User',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('text', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name': 'Profile',
                'db_table': 'profile',
            },
        ),
        migrations.CreateModel(
            name='RelateUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('follow_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_target', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'relateuser',
                'db_table': 'relateuser',
            },
        ),
    ]
