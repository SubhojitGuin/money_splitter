from django.urls import path
from . import views
#app_name = 'expenses'
urlpatterns = [
    path('<int:pk>/', views.expense_list, name='expense_list'),
    path('<int:pk>/create/', views.create_expense, name='create_expense'),
    path('<int:expense_id>/<int:group_id>/split/', views.split_expense, name='split_expense'),
    path('net_owed/<int:group_id>/', views.net_amount_owed, name='net_amount_owed')
]