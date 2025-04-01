import requests
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
from students.models import StudentProfile
from django.contrib.auth import authenticate, logout

class CamundaLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Проверяем, существует ли пользователь в Django
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Запрос к Camunda REST API
        camunda_url = f"http://localhost:8080/engine-rest/user/{username}/profile"
        response = requests.get(camunda_url)

        if response.status_code != 200:
            return Response({"error": "User not found in Camunda"}, status=status.HTTP_404_NOT_FOUND)

        # Получаем StudentProfile, если он существует
        try:
            student_profile = StudentProfile.objects.get(user=user)
            student_data = {
                "kbtu_id": student_profile.kbtu_id,
                "school": student_profile.school,
                "speciality": student_profile.speciality,
                "course": student_profile.course,
                "phone": student_profile.telephone_number,
            }
        except StudentProfile.DoesNotExist:
            student_data = None  # Если профиля нет, не передаем данные

        return Response({
            "message": "Login successful",
            "username": username,
            "student_profile": student_data
        }, status=status.HTTP_200_OK)


class CamundaLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)



CAMUNDA_BASE_URL = "http://localhost:8080/engine-rest"

@api_view(["POST"])
def start_process(request):
    student_id = request.data.get("student_id", "unknown")
    initiator = request.data.get("initiator", "demo") 

    data = {
        "variables": {
            "student_id": {"value": student_id, "type": "String"},
            "initiator": {"value": initiator, "type": "String"}  
        }
    }
    
    response = requests.post(f"{CAMUNDA_BASE_URL}/process-definition/key/Process_student/start", json=data)

    if response.status_code in [200, 201]:
        return Response({"message": "Process started!", "processInstanceId": response.json().get("id")})
    return Response(response.json(), status=response.status_code)

@api_view(["GET"])
def get_user_tasks(request):
    user_id = request.query_params.get("user_id", "some_user") 
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
# @csrf_exempt
# def upload_task_attachment(request, task_id):
#     if request.method == "POST":
#         if "file" not in request.FILES:
#             return JsonResponse({"error": "Файл не передан!"}, status=400)

#         file = request.FILES["file"]
#         file_data = file.read()
#         encoded_file = base64.b64encode(file_data).decode("utf-8")

#         camunda_url = f"http://localhost:8080/engine-rest/task/{task_id}/attachment/create"
#         headers = {"Content-Type": "application/json"}

#         payload = {
#             "name": file.name,
#             "type": file.content_type,
#             "taskId": task_id,
#             "content": encoded_file,
#         }

#         response = requests.post(camunda_url, json=payload, headers=headers)

#         if response.status_code == 200 or response.status_code == 204:
#             return JsonResponse({"message": "Файл успешно загружен!"})
#         else:
#             return JsonResponse({"error": response.json()}, status=response.status_code)

#     return JsonResponse({"error": "Метод не поддерживается!"}, status=405)

# @api_view(["GET"])
# def download_task_attachment(request, task_id, attachment_id):
#     """Скачивает файл, прикрепленный к задаче"""
#     response = requests.get(f"{CAMUNDA_BASE_URL}/task/{task_id}/attachment/{attachment_id}/data", stream=True)
    
#     if response.status_code == 200:
#         return FileResponse(response.raw, as_attachment=True, filename=f"attachment_{attachment_id}.bin")
#     return Response(response.json(), status=response.status_code)
