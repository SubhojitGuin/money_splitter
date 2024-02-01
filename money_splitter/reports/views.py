# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Report, ReportExpense, ReportPayment
from .forms import ReportForm

@login_required
def report_list(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, 'reports/report_list.html', {'reports': reports})

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            expenses = Expense.objects.filter(group=request.user.groups.first(), created_at__range=[form.cleaned_data['start_date'], form.cleaned_data['end_date']])
            report.expenses.set(expenses)
            payments = Payment.objects.filter(expense__in=report.expenses.all())
            for payment in payments:
                report.payments.add(payment)
            return redirect('reports:report_list')
    else:
        form = ReportForm()
    return render(request, 'reports/create_report.html', {'form': form})

@login_required
def report_detail(request, report_id):
    report = Report.objects.get(id=report_id)
    return render(request, 'reports/report_detail.html', {'report': report})