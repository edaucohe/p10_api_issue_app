from django.conf import settings
from django.db import models


# Create your models here.
class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACK_END = ("BACK-END", "Back-End")
        FRONT_END = ("FRONT-END", "Front-End")
        IOS = ("IOS", "iOS")
        ANDROID = ("ANDROID", "Android")

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    created_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=15, choices=ProjectType.choices, verbose_name="type of project")
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
