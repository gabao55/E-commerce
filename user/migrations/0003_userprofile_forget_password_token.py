# Generated by Django 3.2.7 on 2021-11-01 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210920_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='forget_password_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]