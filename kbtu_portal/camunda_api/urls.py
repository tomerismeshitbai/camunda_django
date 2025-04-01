from django.urls import path
from .views import (
    start_process,
    get_user_tasks,
    get_task_details,
    get_dean_task_details,
    complete_task,
    CamundaLoginView,
    CamundaLogoutView,
    upload_attachment,
    view_attachment,
    get_attachments
)

urlpatterns = [
    path("start-process/", start_process, name="start-process"),
    path("tasks/", get_user_tasks, name="get-user-tasks"),
    path("task/<str:task_id>/", get_task_details, name="get-task-details"),
    path("task_dean/<str:task_id>/", get_dean_task_details, name="get-dean-task-details"),
    path("task/<str:task_id>/complete/", complete_task, name="complete-task"),
    path("login/", CamundaLoginView.as_view(), name='camunda_login'),
    path("logout/", CamundaLogoutView.as_view(), name='camunda_logout'),
    path('tasks/<int:task_id>/upload/attachments/', upload_attachment, name='upload_attachment'),
    # path("tasks/<int:task_id>/attachments/", get_attachments, name="get_attachments"),
    # path("attachments/<int:attachment_id>/view/", view_attachment, name="view_attachment"),

]
