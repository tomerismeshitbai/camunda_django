from django.db import models
from students.models import StudentProfile
from dean_managers.models import ManagerProfile

class Appointment(models.Model):
    COURSE_CHOICES = [
        ('1 course', '1 course'),
        ('2 course', '2 course'),
        ('3 course', '3 course'),
        ('4 course', '4 course'),
        ('5-7 course', '5-7 course'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending',
    )
    rejection_reason = models.TextField(null=True, blank=True)

    manager = models.ForeignKey(ManagerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    

    def get_course(self):
        return self.student.course  

    def get_specialty(self):
        return self.student.speciality  
    
    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'


class AppointmentManager(models.Manager):
    def available_for_manager(self):
        """
        Метод для выбора доступных менеджеров (например, которые не заняты)
        """
        return self.filter(manager__isnull=True)

    def get_appointments_by_manager(self, manager_id):
        """
        Метод для получения записей для конкретного менеджера
        """
        return self.filter(manager__id=manager_id)
