from django.db import models

class Task(models.Model):
    process_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Task in Process {self.process_id}"

class Attachment(models.Model):
    task = models.ForeignKey('Task', related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')

    def __str__(self):
        return f"Attachment for Task {self.task.id}"

