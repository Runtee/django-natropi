# Generated by Django 5.0.6 on 2024-06-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='days_passed',
            field=models.IntegerField(default=0),
        ),
    ]
