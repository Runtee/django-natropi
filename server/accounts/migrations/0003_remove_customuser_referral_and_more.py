# Generated by Django 5.0.6 on 2024-06-02 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_referral_bonus_customuser_referral_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='referral',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='referral_bonus',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='referral_code',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='referral_count',
        ),
    ]
