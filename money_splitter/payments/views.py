# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from .forms import PaymentForm
from expenses.models import Expense


@login_required
def payment_list(request):
    payments = Payment.objects.filter(paidby_id=request.user.id) | Payment.objects.filter(paidto_id=request.user.id)
    return render(request, 'payments/payment_list.html', {'payments1': payments})

@login_required
def create_payment(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.payer = request.user
            payment.expense = expense
            payment.save()
            return redirect('payments:payment_list')
    else:
        form = PaymentForm()
    return render(request, 'payments/create_payment.html', {'form': form, 'expense': expense})