# Generated by Django 5.0.1 on 2024-02-03 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_alter_payment_paid_by_alter_payment_paid_to'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paid_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_made', to='users.customuser'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paid_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_received', to='users.customuser'),
        ),
    ]