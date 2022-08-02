from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from projects.models import Project


class User(AbstractUser):
    pass


class Contributor(models.Model):
    TYPE_OF_ROLE = [
        ("AUTHOR", "Author"),
        ("CONTRIBUTOR", "Contributor")
    ]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=TYPE_OF_ROLE, verbose_name='Type of role')
