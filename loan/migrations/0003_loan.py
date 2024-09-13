# Generated by Django 4.2 on 2024-09-13 09:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loan', '0002_upfront'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_requested', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('repayment_term_months', models.IntegerField()),
                ('applied_date', models.DateField(default=datetime.datetime.now)),
                ('upfronts', models.ManyToManyField(blank=True, related_name='loans', to='loan.upfront')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
