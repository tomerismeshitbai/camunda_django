from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    kbtu_id = models.CharField(max_length=10, default="21B000000", unique=True)
    email = models.EmailField(unique=True)
    school = models.CharField(max_length=50, default="SITE")
    speciality = models.CharField(max_length=50, default="IS")
    course = models.IntegerField(default=4)
    telephone_number = models.CharField(max_length=20, default="87777777777")
    role = models.CharField(max_length=20, default="student")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.kbtu_id})"
