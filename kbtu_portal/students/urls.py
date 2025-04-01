from django.urls import path
from students.views import StudentProfileDetailView, StudentProfileUpdateView

urlpatterns = [
    path('<int:id>/', StudentProfileDetailView.as_view(), name='student-detail'),
    path('<int:id>/edit/', StudentProfileUpdateView.as_view(), name='student-edit'),
]
