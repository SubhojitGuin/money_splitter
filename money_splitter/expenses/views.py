from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense
from payments.models import Payment
from .forms import ExpenseForm
from groups.models import Group
from django.contrib.auth import get_user_model


@login_required
def expense_list(request, pk):
    expenses = Expense.objects.filter(group=pk)
    group_name = Group.objects.get(id=pk).name

    total = []
    payment_to_names = []
    group = Group.objects.get(id=pk)

    # payment_to_id_list = Payment.objects.filter(
    #     paidby_id=request.user.id, expense__group=group
    # ).paidto_id

    payment_to_id_list = Payment.objects.filter(
        paidby_id=request.user.id, expense__group=group
    ).values_list('paidto_id', flat=True).distinct()

    # payment_to_id_list = Payment.objects.filter(
    #     paidby_id=request.user.id, expense__group=group
    # ).paid_to_name

    for payment_to_id in payment_to_id_list:
        if request.user.id == payment_to_id:
            continue
        total_due = calculate_total_due(request, request.user.id, payment_to_id, pk)
        total.append(total_due)
        payment_to_names.append(get_user_model().objects.get(id=payment_to_id).username)

    l = list(zip(payment_to_names, total))
    return render(request, 'expenses/expense_list.html',
                  {'expenses': expenses, 'id': pk, 'group_name': group_name,
                   'l': total})


def calculate_total_due(request, paid_by_id, paid_to_id, group_id):
    # paid_by = CustomUser.objects.get(id=paid_by_id)
    # paid_to = CustomUser.objects.get(id=paid_to_id)
    group = Group.objects.get(id=group_id)

    payments_from_paid_by_to_paid_to = Payment.objects.filter(
        paidby_id=paid_by_id, paidto_id=paid_to_id, expense__group=group
    )
    payments_from_paid_to_to_paid_by = Payment.objects.filter(
        paidby_id=paid_to_id, paidto_id=paid_by_id, expense__group=group
    )

    total_due = sum(
        [payment.amount for payment in payments_from_paid_by_to_paid_to]) - sum(
        [payment.amount for payment in payments_from_paid_to_to_paid_by])

    return total_due


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
        payment.paidby_id = member.id
        payment.paidto_id = expense.creator.id

        payment.save()


def split_expense(request, expense_id, group_id):
    payments = Payment.objects.filter(expense_id=expense_id)
    ppp = payments[0].paid_by_names
    return render(request, 'expenses/split_expense.html',
                  {'payments': payments, 'id': group_id, 'ppp': ppp,
                   'Total': Expense.objects.get(id=expense_id)})
