from django.db import models
from students.models import StudentProfile
from datetime import date


class DocumentSample(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    desc = models.TextField(verbose_name="Description", blank=True, null=True)
    file = models.FileField(upload_to='documents/', verbose_name="File")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")  

    def __str__(self):
        return self.name


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
        full_name = f"{self.student.last_name} {self.student.first_name} {self.student.middle_name if self.student.middle_name else ''}".strip()
        return f"Заявление {full_name} ({self.student.kbtu_id})"



class InvitationLetter(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True, blank=True)
    
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    course = models.PositiveIntegerField(null=True, blank=True)
    speciality = models.CharField(max_length=255, blank=True)
    
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
         if self.student and self.student.user:
            return f"Приглашение для {self.student.user.get_full_name()} в {self.organization_name}"
         else:
            return f"Приглашение для неопределенного студента в {self.organization_name}"

