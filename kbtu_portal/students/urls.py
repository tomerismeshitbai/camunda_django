from django.urls import path
from students.views import StudentProfileDetailView, StudentProfileUpdateView, StudentProfileByUserView

urlpatterns = [
    path('<int:id>/', StudentProfileDetailView.as_view(), name='student-detail'),
    path('<int:id>/edit/', StudentProfileUpdateView.as_view(), name='student-edit'),
    path('user/<int:user_id>/', StudentProfileByUserView.as_view(), name='student-by-user'),
]
