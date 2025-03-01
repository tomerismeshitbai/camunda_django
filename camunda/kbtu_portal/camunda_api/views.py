import requests
# import base64
# import mimetypes
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

CAMUNDA_BASE_URL = "http://localhost:8080/engine-rest"

@api_view(["POST"])
def start_process(request):
    """Запускает процесс и передает инициатора"""
    student_id = request.data.get("student_id", "unknown")
    initiator = request.data.get("initiator", "default_user")  # кто стартует процесс

    data = {
        "variables": {
            "student_id": {"value": student_id, "type": "String"},
            "initiator": {"value": initiator, "type": "String"}  # сохраняем пользователя
        }
    }
    
    response = requests.post(f"{CAMUNDA_BASE_URL}/process-definition/key/Process_student/start", json=data)

    if response.status_code in [200, 201]:
        return Response({"message": "Процесс запущен!", "processInstanceId": response.json().get("id")})
    return Response(response.json(), status=response.status_code)


@api_view(["GET"])
def get_user_tasks(request):
    """Получает список активных задач для пользователя"""
    user_id = request.query_params.get("user_id", "some_user")  # Получаем ID пользователя
    response = requests.get(f"{CAMUNDA_BASE_URL}/task", params={"assignee": user_id})

    if response.status_code == 200:
        return Response(response.json())
    return Response(response.json(), status=response.status_code)


@api_view(["GET"])
def get_task_details(request, task_id):
    """Получает данные конкретной задачи (переменные формы)"""
    response = requests.get(f"{CAMUNDA_BASE_URL}/task/{task_id}/form-variables")

    if response.status_code == 200:
        return Response(response.json())
    return Response(response.json(), status=response.status_code)


@api_view(["POST"])
def complete_task(request, task_id):
    """Завершает задачу и отправляет данные в Camunda"""
    data = {"variables": request.data.get("variables", {})}
    response = requests.post(f"{CAMUNDA_BASE_URL}/task/{task_id}/complete", json=data)

    if response.status_code in [200, 204]:
        return Response({"message": "Задача завершена!"})
    return Response(response.json(), status=response.status_code)












# @api_view(["POST"])
# @parser_classes([MultiPartParser])
# def upload_task_file(request, task_id):
#     file = request.FILES.get("file")
#     if not file:
#         return Response({"error": "Файл не передан"}, status=400)

#     encoded_file = base64.b64encode(file.read()).decode("utf-8")
#     mime_type, _ = mimetypes.guess_type(file.name)
#     mime_type = mime_type or "application/octet-stream"  # Устанавливаем MIME-тип, если не определён

#     # Загружаем сам файл как переменную типа Bytes
#     file_data = {
#         "modifications": {
#             "documentData": {
#                 "value": encoded_file,
#                 "type": "Bytes",
#                 "valueInfo": {"mimeType": mime_type}
#             }
#         }
#     }

#     file_name_data = {
#         "modifications": {
#             "documentFilename": {
#                 "value": file.name,
#                 "type": "String"
#             }
#         }
#     }

#     # Сначала загружаем сам файл
#     file_response = requests.post(f"{CAMUNDA_BASE_URL}/task/{task_id}/variables", json=file_data)

#     # Затем загружаем имя файла как отдельную переменную
#     name_response = requests.post(f"{CAMUNDA_BASE_URL}/task/{task_id}/variables", json=file_name_data)

#     if file_response.status_code in [200, 204] and name_response.status_code in [200, 204]:
#         return Response({"message": "Файл успешно загружен!"})
#     return Response({"error": "Ошибка при загрузке файла"}, status=500)

# @api_view(["GET"])
# def view_task_file(request, task_id):
#     file_response = requests.get(f"{CAMUNDA_BASE_URL}/task/{task_id}/variables/documentData")
#     name_response = requests.get(f"{CAMUNDA_BASE_URL}/task/{task_id}/variables/documentFilename")

#     if file_response.status_code == 200 and name_response.status_code == 200:
#         file_data = file_response.json()
#         name_data = name_response.json()

#         encoded_file = file_data.get("value")
#         filename = name_data.get("value", "document")  # Используем сохранённое имя файла

#         content_type, _ = mimetypes.guess_type(filename)
#         if not content_type:
#             content_type = file_data.get("valueInfo", {}).get("mimeType", "application/octet-stream")

#         if encoded_file:
#             file_content = base64.b64decode(encoded_file)
#             response = HttpResponse(file_content, content_type=content_type)
#             response["Content-Disposition"] = f'attachment; filename="{filename}"'
#             return response

#     return Response({"error": "Файл не найден"}, status=404)
