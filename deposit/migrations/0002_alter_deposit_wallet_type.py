# Generated by Django 5.0.6 on 2024-09-29 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='wallet_type',
            field=models.CharField(blank=True, choices=[('USDT', 'USDT'), ('LTC', 'Litecoin'), ('BTC', 'Bitcoin'), ('XRP', 'XRP'), ('ETH', 'ETHERUM')], max_length=100, null=True),
        ),
    ]
