from django.urls import path
from . import views
#app_name = 'expenses'
urlpatterns = [
    path('<int:pk>/', views.expense_list, name='expense_list'),
    path('<int:pk>/create/', views.create_expense, name='create_expense'),
]