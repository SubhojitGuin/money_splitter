# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from groups.models import Group
from expenses.models import Expense


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='notifications')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='notifications')
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE,
                                related_name='notifications', null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification {self.id} for {self.user} in {self.group}'
