# Generated by Django 4.2 on 2024-09-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
