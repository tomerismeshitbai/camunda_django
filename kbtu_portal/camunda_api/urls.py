from django.urls import path
from .views import (
    start_process,
    get_user_tasks,
    get_task_details,
    complete_task,
    CamundaLoginView,
    CamundaLogoutView,
    # upload_task_attachment,
    # download_task_attachment,
)

urlpatterns = [
    path("start-process/", start_process, name="start-process"),
    path("tasks/", get_user_tasks, name="get-user-tasks"),
    path("task/<str:task_id>/", get_task_details, name="get-task-details"),
    path("task/<str:task_id>/complete/", complete_task, name="complete-task"),
    path("login/", CamundaLoginView.as_view(), name='camunda_login'),
    path("logout/", CamundaLogoutView.as_view(), name='camunda_logout'),

    # path("task/<str:task_id>/upload/", upload_task_attachment, name="upload-task-attachment"),
    # path("task/<str:task_id>/download/<str:attachment_id>/", download_task_attachment, name="download-task-attachment"),
]
