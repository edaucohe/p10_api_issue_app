from django.conf import settings
from django.db import models


# Create your models here.
from issues.models import Issue


class Comment(models.Model):
    description = models.TextField(max_length=2000)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
