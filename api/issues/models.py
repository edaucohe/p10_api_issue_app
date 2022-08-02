from django.conf import settings
from django.db import models


# Create your models here.
from projects.models import Project


class Issue(models.Model):
    TYPE_OF_TAG = [
        ("BUG", "Bug"),
        ("ENHANCEMENT", "Enhancement"),
        ("TASK", "Task")
    ]

    TYPE_OF_PRIORITY = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High")
    ]

    TYPE_OF_STATUS = [
        ("TODO", "To do"),
        ("IN_PROGRESS", "In progress"),
        ("DONE", "Done")
    ]

    title = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    created_time = models.DateTimeField(auto_now_add=True)

    tag = models.CharField(max_length=20, choices=TYPE_OF_TAG, verbose_name="type of tag")
    priority = models.CharField(max_length=20, choices=TYPE_OF_PRIORITY, verbose_name="type of priority")
    status = models.CharField(max_length=20, choices=TYPE_OF_STATUS, verbose_name="type of status")

    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author")
    assignee_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=author_user,
        related_name="assignee")
