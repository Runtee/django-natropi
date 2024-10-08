# Generated by Django 5.0.6 on 2024-09-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawalsmade',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='withdrawalsmade',
            name='message',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='withdrawalsmade',
            name='method',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='withdrawalsmade',
            name='wallet_type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
