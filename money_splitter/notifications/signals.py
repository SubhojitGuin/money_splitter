from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from expenses.models import Expense


@receiver(post_save, sender=Expense)
def create_notification(sender, instance, created, **kwargs):
    if created:
        for user in instance.group.members.exclude(id=instance.creator.id):
            Notification.objects.create(user=user, group=instance.group, expense=instance)