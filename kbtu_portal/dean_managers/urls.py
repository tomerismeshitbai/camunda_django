from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManagerProfileViewSet

router = DefaultRouter()
router.register(r'manager-profiles', ManagerProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
