from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

# Create your models here.

class Department(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)

    def generate_verification_token(self):
        token = get_random_string(length=32)
        self.verification_token = token
        self.save()
        return token

    def __Str__(self):
        return self.username
    



    
