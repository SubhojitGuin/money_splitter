# Generated by Django 5.0.1 on 2024-02-04 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0014_payment_paid_by_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='paid_to_names',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
