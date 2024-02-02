from datetime import timezone, datetime

from django.db import models
from django.contrib.auth.models import User
from groups.models import Group

class Expense(models.Model):
    name = models.CharField(max_length=100, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenses', default=None)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses', default=None)
    split_method = models.CharField(max_length=10, choices=(('equal', 'Equal'), ('custom', 'Custom')), default='default_value')
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.name