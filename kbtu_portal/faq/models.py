from django.db import models
from django.utils import timezone

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    course = models.IntegerField()
    published = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.question
