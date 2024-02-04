from django.db import models
from expenses.models import Expense
from users.models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

#User = get_user_model()

# Create your models here.
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments_made' , null=True)
    paid_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments_received', null=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='payments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.amount} paid by {self.paid_by} to {self.paid_to} for {self.expense}'