from django.conf import settings
from django.db import models


# Create your models here.
class Project(models.Model):
    TYPE_OF_PROJECT = [
        ("BACK-END", "Back-End"),
        ("FRONT-END", "Front-End"),
        ("IOS", "iOS"),
        ("ANDROID", "Android")
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    created_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=15, choices=TYPE_OF_PROJECT, verbose_name="type of project")
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
