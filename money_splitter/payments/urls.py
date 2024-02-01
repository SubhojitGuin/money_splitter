from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('create/<int:expense_id>/', views.create_payment, name='create_payment'),
]