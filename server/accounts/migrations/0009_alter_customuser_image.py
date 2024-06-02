# Generated by Django 5.0.6 on 2024-06-02 20:55

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customuser_referral_bonus_customuser_referral_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='assets/img/logo/logo.jpg', upload_to=accounts.models.profile_image_path),
        ),
    ]
