from django.db import models
from django.contrib.auth.models import User

class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager_profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    school = models.CharField(max_length=50, default="SITE")
    phone_number = models.CharField(max_length=20, default="87770001122")
    role = models.CharField(max_length=20, default="dean manager")
    position = models.CharField(max_length=100, default="Dean Manager")  

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"  
