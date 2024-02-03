from django.contrib import messages
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense
from payments.models import Payment
from .forms import ExpenseForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
@login_required
def expense_list(request, pk):
    expenses = Expense.objects.filter(group=pk)
    return render(request, 'expenses/expense_list.html',
                  {'expenses': expenses, 'id': pk})


@login_required
def create_expense(request, pk):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.creator = request.user
            expense.group_id = pk
            with transaction.atomic():
                expense.save()
                split_expense(request, expense.id)
            messages.success(request, 'Expense created successfully!')
            return redirect('expenses:render_form', expense_id=expense.id)
    else:
        form = ExpenseForm()
    return render(request, 'expenses/create_expense.html', {'form': form, 'id': pk})

@receiver(post_save, sender=Expense)
def expense_created(request, sender, instance, created, **kwargs):
    if created:
        split_expense(request, instance.id)

def render_form(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, group__members=request.user)
    return render(request, 'expenses/split_expense.html', {'expense': expense})


@login_required
def split_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, group__members=request.user)
    if request.method == 'POST':
        # Perform the splitting logic here
        total_amount = expense.amount
        members = expense.group.members.all()
        member_count = members.count()
        amount_per_member = total_amount / member_count
        for member in members:
            payment = Payment(amount=amount_per_member, expense=expense,
                              paid_by=member, paid_to=request.user)
            payment.save()
        expense.delete()
        return redirect('expenses:expense_list', pk=expense.group_id)
    else:
        return render(request, 'expenses/split_expense.html', {'expense': expense})
        # return redirect('expenses:expense_list')
# Compare this snippet from money_splitter/users/views.py: