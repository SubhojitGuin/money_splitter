# Generated by Django 5.0.1 on 2024-02-01 22:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='expense',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='paid_by',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='paid_to',
        ),
        migrations.AddField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='expense',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='created_expenses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='expense',
            name='group',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='groups.group'),
        ),
        migrations.AddField(
            model_name='expense',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='expense',
            name='split_method',
            field=models.CharField(choices=[('equal', 'Equal'), ('custom', 'Custom')], default='default_value', max_length=10),
        ),
    ]
