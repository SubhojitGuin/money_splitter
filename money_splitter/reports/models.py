from django.db import models
from django.contrib.auth.models import User
from groups.models import Group
from expenses.models import Expense
from payments.models import Payment

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='reports')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report {self.id} for {self.user} in {self.group}'

class ReportExpense(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='expenses')
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='report_expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.expense} in {self.report}'

class ReportPayment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='payments')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='report_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.payment} in {self.report}'
