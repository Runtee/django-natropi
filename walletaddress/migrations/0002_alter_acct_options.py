# Generated by Django 5.0.6 on 2024-06-08 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walletaddress', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='acct',
            options={'verbose_name': 'Payment Account', 'verbose_name_plural': 'Payment Accounts'},
        ),
    ]
