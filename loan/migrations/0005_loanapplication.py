# Generated by Django 4.2 on 2024-09-13 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loan', '0004_upfront_loan_amount_requested'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_requested', models.DecimalField(decimal_places=2, max_digits=10)),
                ('approved', models.BooleanField(default=False)),
                ('date_applied', models.DateTimeField(auto_now_add=True)),
                ('loan_term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.loanterm')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]