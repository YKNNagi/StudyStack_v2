from django.db import models
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Study(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    content = models.CharField(max_length=200)
    tags = models.ManyToManyField(
        Tag,
        blank=True
        )
    created_at = models.DateTimeField(auto_now_add=True)