from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from projects.models import Project


class User(AbstractUser):
    pass


class Contributor(models.Model):
    class Role(models.TextChoices):
        Author = ("AUTHOR", "Author")
        Contributor = ("CONTRIBUTOR", "Contributor")

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices, verbose_name='role')
