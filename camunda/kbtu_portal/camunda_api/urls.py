from django.urls import path
from .views import start_process, upload_task_file, view_task_file

urlpatterns = [
    path("start-process/", start_process, name="start-process"),
    path("task/<str:task_id>/upload-file/", upload_task_file, name="upload-task-file"),
    path("task/<str:task_id>/view-file/", view_task_file, name="view-task-file"),
]
