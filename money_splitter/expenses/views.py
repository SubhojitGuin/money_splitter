from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(group__members=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.creator = request.user
            expense.save()
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/create_expense.html', {'form': form})

@login_required
def split_expense(request):
    if request.method == 'POST':
        for expense_id in request.POST:
            if expense_id.startswith('split_'):
                split = int(request.POST[expense_id])
                expense_id = expense_id.replace('split_', '')
                expense = Expense.objects.get(id=expense_id)
                # Perform the splitting logic here
        return redirect('expenses:expense_list')
