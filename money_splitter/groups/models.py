from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
#
CustomUser = get_user_model()


# class Group(models.Model):
#     name = models.CharField(max_length=100)
#     members = models.ManyToManyField(User, related_name='groups')
#     creator = models.ForeignKey(User, on_delete=models.CASCADE,
#                                 related_name='created_groups')
class Group(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                related_name='created_groups')
    members = models.ManyToManyField(CustomUser, related_name='member_groups')

    def __str__(self):
        return self.name
