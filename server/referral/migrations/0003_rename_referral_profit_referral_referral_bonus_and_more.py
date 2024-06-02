# Generated by Django 5.0.6 on 2024-06-02 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0002_referral_referral_code_alter_referral_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referral',
            old_name='referral_profit',
            new_name='referral_bonus',
        ),
        migrations.RemoveField(
            model_name='referral',
            name='referred_user',
        ),
        migrations.AddField(
            model_name='referral',
            name='referral_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='referral',
            name='referred_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referrals', to='referral.referral'),
        ),
    ]
