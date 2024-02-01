from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

from groups.models import Group


# class CustomUser(AbstractUser):
#     pass

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
