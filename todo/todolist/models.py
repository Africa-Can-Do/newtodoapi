from django.db import models

# Create your models here.

from django.db import models
from account.models import CustomUser

class Todo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

