from django.urls import path
from .views import start_process, get_user_tasks, get_task_details, complete_task

urlpatterns = [
    path("start-process/", start_process, name="start-process"),
    # path("task/<str:task_id>/upload-file/", upload_task_file, name="upload-task-file"),
    # path("task/<str:task_id>/view-file/", view_task_file, name="view-task-file"),
    
    path("tasks/", get_user_tasks, name="get-user-tasks"),  # Получение списка задач
    path("tasks/<str:task_id>/", get_task_details, name="get-task-details"),  # Данные задачи
    path("tasks/<str:task_id>/complete/", complete_task, name="complete-task"),  # Завершение задачи
]
