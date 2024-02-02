from django.urls import path
from . import views
#app_name = 'expenses'
urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('create/', views.create_expense, name='create_expense'),
]