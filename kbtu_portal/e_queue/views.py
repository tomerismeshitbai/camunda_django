from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        """
        Получаем записи, доступные для данного пользователя.
        Можно изменить, например, чтобы показывать только записи, связанные с менеджером.
        """
        queryset = Appointment.objects.all()
        manager_id = self.request.query_params.get('manager', None)
        if manager_id:
            queryset = queryset.filter(manager__id=manager_id)
        return queryset
