from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense
from payments.models import Payment
from .forms import ExpenseForm
from django.contrib.auth import get_user_model


@login_required
def expense_list(request, pk):
    expenses = Expense.objects.filter(group=pk)
    return render(request, 'expenses/expense_list.html',
                  {'expenses': expenses, 'id': pk})


@login_required
def create_expense(request, pk):
    expense = None
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.creator = request.user
            expense.group_id = pk
            expense.save()
            split_exp(request, expense_id=expense.id)
            # split_expense(request , expense.id)
            # return redirect('expenses:expense_list', pk=pk)
    else:
        form = ExpenseForm()
    return render(request, 'expenses/create_expense.html',
                  {'form': form, 'id': pk, 'expense': expense})


# def split_expense(request , expense_id):
#     expense = Expense.objects.get(id=expense_id)
#     if expense.split_method == 'equal':
#         split_equal(request , expense)
#
# def split_equal(request , expense):
#     total_amount = expense.amount
#     members = expense.group.members.all()
#     member_count = members.count()
#     amount_per_member = total_amount / member_count
#     user_paid_by = User.objects.get(username='username1')
#     user_paid_to = User.objects.get(username='username2')
#     for member in members:
#         payment = Payment(amount=amount_per_member, expense=expense,
#                           paid_by=request.user, paid_to=member)
#         payment.save()
#     expense.delete()
#
def split_exp(request, expense_id):
    expense = Expense.objects.get(id=expense_id)

    members = expense.group.members.all()
    split_amount = expense.amount / members.count()
    for member in members:
        # if member == expense.creator:
        # continue
        payment = Payment()
        payment.expense = expense
        payment.amount = split_amount
        # payment.paid_to = member
        # payment.paid_by = expense.creator
        payment.paid_by_names = member.username
        payment.paid_to_names = expense.creator.username

        payment.save()


def split_expense(request, expense_id, group_id):
    payments = Payment.objects.filter(expense_id=expense_id)
    return render(request, 'expenses/split_expense.html',
                  {'payments': payments, 'id': group_id})
