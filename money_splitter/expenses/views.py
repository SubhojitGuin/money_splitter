from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from payments.models import Payment
from .forms import ExpenseForm


@login_required
def expense_list(request, pk):
    expenses = Expense.objects.filter(group=pk)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses , 'id':pk})


@login_required
def create_expense(request, pk):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.creator = request.user
            expense.group_id = pk
            expense.save()
            split_expense(request , expense.id)
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/create_expense.html', {'form': form, 'id': pk})

def split_expense(request , expense_id):
    expense = Expense.objects.get(id=expense_id)
    if expense.split_method == 'equal':
        split_equal(request , expense)

def split_equal(request , expense):
    total_amount = expense.amount
    members = expense.group.members.all()
    member_count = members.count()
    amount_per_member = total_amount / member_count
    for member in members:
        payment = Payment(amount=amount_per_member, expense=expense,
                          paid_by=request.user, paid_to=member)
        payment.save()
    expense.delete()
