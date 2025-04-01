from django.db import models
from students.models import StudentProfile
from faq.models import FAQ 

class FAQRequest(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(upload_to='faq_attachments/', blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    is_answered = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала сохраняем объект
        if self.published and self.answer:  # Проверяем, опубликован ли он и есть ли ответ
            FAQ.objects.get_or_create(
                question=self.description,
                answer=self.answer
            )

    def __str__(self):
        return self.topic
