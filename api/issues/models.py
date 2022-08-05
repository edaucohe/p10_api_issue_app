from django.conf import settings
from django.db import models


# Create your models here.
from projects.models import Project


class Issue(models.Model):
    class Tag(models.TextChoices):
        BUG = ("BUG", "Bug")
        ENHANCEMENT = ("ENHANCEMENT", "Enhancement")
        TASK = ("TASK", "Task")

    class Priority(models.TextChoices):
        LOW = ("LOW", "Low")
        Medium = ("MEDIUM", "Medium")
        HIGH = ("HIGH", "High")

    class Status(models.TextChoices):
        TODO = ("TODO", "To do")
        IN_PROGRESS = ("IN_PROGRESS", "In progress")
        DONE = ("DONE", "Done")

    title = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    created_time = models.DateTimeField(auto_now_add=True)

    tag = models.CharField(max_length=20, choices=Tag.choices, verbose_name="tag")
    priority = models.CharField(max_length=20, choices=Priority.choices, verbose_name="priority")
    status = models.CharField(max_length=20, choices=Status.choices, verbose_name="status")

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
