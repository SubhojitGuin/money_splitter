# Generated by Django 5.0.1 on 2024-02-03 22:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_alter_payment_paid_by_alter_payment_paid_to'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paid_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_made', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paid_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_received', to=settings.AUTH_USER_MODEL),
        ),
    ]