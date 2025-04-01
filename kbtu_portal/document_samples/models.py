from django.db import models
from students.models import StudentProfile
from datetime import date


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    credits_kz = models.IntegerField()
    credits_ects = models.IntegerField()
    retake = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name} ({self.credits_kz} KZ / {self.credits_ects} ECTS)"

class CourseRegistrationApplication(models.Model):
    SEMESTER_CHOICES = [
        ('Осенний', 'Осенний'),
        ('Весенний', 'Весенний'),
        ('Летний', 'Летний'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    courses = models.ManyToManyField(Course)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявление {self.student.full_name} ({self.student.kbtu_id})"


class InvitationLetter(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)  
    start_date = models.DateField()
    end_date = models.DateField()  
    supervisor_name = models.CharField(max_length=255)  
    supervisor_position = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def current_year(self):
        return date.today().year  

    def __str__(self):
        return f"Приглашение для {self.student.user.get_full_name()} в {self.organization_name}"

