from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('mark_read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
]