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
from dean_managers.models import ManagerProfile
from django.contrib.auth import authenticate, logout
from .models import Task, Attachment
from django.shortcuts import get_object_or_404
import mimetypes

class CamundaLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user_id = user.id

        # Получаем данные пользователя из Camunda
        camunda_url = f"http://localhost:8080/engine-rest/user/{username}/profile"
        response = requests.get(camunda_url)

        if response.status_code != 200:
            return Response({"error": "User not found in Camunda"}, status=status.HTTP_404_NOT_FOUND)

        role = None
        user_data = {}

        # Проверяем, есть ли профиль студента
        student_profile = StudentProfile.objects.filter(user_id=user_id).first()
        if student_profile:
            role = "student"
            user_data = {
                "id": student_profile.id,
                "first_name": student_profile.first_name,
                "last_name": student_profile.last_name,
                "kbtu_id": student_profile.kbtu_id,
                "email": student_profile.email,
                "school": student_profile.school,
                "speciality": student_profile.speciality,
                "course": student_profile.course,
                "telephone_number": student_profile.telephone_number
            }

        # Проверяем, есть ли профиль менеджера
        manager_profile = ManagerProfile.objects.filter(user_id=user_id).first()
        if manager_profile:
            role = "dean manager"
            user_data = {
                "first_name": manager_profile.first_name,
                "last_name": manager_profile.last_name,
                "email": manager_profile.email,
                "school": manager_profile.school,
                "phone_number": manager_profile.phone_number,
                "position": manager_profile.position
            }

        if role is None:
            role = "unknown"

        return Response({
            "message": "Login successful",
            "username": username,
            "user_id": user_id,
            "role": role,
            "user_data": user_data
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
        process_instance_id = response.json().get("id") 
        task = Task.objects.create(process_id=process_instance_id)
        return Response({"message": "Process started!", "processInstanceId": response.json().get("id"), "taskId": task.id})
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
    response = requests.get(f"{CAMUNDA_BASE_URL}/task/{task_id}/form-variables")

    if response.status_code == 200:
        return Response(response.json())
    return Response(response.json(), status=response.status_code)

@api_view(["GET"])
def get_dean_task_details(request, task_id):
    response = requests.get(f"{CAMUNDA_BASE_URL}/task/{task_id}/form-variables")
    
    if response.status_code == 200:
        task_details = response.json()
        source_process_id = task_details.get("sourceProcessId", {}).get("value")

        if source_process_id:
            try:
                task = Task.objects.get(process_id=source_process_id)
            except Task.DoesNotExist:
                return Response({"message": "Task with matching process_id not found"}, status=status.HTTP_404_NOT_FOUND)
            
            attachments = Attachment.objects.filter(task=task)
            attachments_data = [{"id": attachment.id, "file_url": attachment.file.url} for attachment in attachments]
            return Response({
                "message": "Attachments found",
                "attachments": attachments_data
            }, status=status.HTTP_200_OK)
        
        return Response({"message": "sourceProcessId not found in Camunda response"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "message": "Error fetching task details from Camunda",
        "error": response.json()
    }, status=response.status_code)


@api_view(["POST"])
def complete_task(request, task_id):
    data = {"variables": request.data.get("variables", {})}
    response = requests.post(f"{CAMUNDA_BASE_URL}/task/{task_id}/complete", json=data)

    if response.status_code in [200, 204]:
        return Response({
            "message": "Задача завершена!",
            "request_data": request.data  
        })
    return Response(response.json(), status=response.status_code)


@api_view(["POST"])
def upload_attachment(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    

    file = request.FILES.get("file")
    
    if not file:
        return Response({"message": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    attachment = Attachment.objects.create(task=task, file=file)
    
    return Response({"message": "Attachment uploaded successfully", "attachment_id": attachment.id}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_attachments(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    attachments = task.attachment_set.all()

    attachment_data = [
        {
            "id": attachment.id,
            "file_url": request.build_absolute_uri(attachment.file.url),
            "view_url": request.build_absolute_uri(f"/attachments/{attachment.id}/view/") 
        }
        for attachment in attachments
    ]

    return Response({"message": "Attachments found", "attachments": attachment_data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def view_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    
    file_path = attachment.file.path
    file_mime_type, _ = mimetypes.guess_type(file_path)

    response = FileResponse(open(file_path, "rb"), content_type=file_mime_type)
    response["Content-Disposition"] = "inline" 
    return response

@api_view(["GET"])
def check_task_by_process_instance(request, process_instance_id):
    # Получаем задачи по user_id и проверяем на "Documents Verification"
    user_id = request.query_params.get("user_id", "DeanManager")  # Получаем user_id из параметров запроса
    response = requests.get(f"http://localhost:8000/api/tasks/", params={"user_id": user_id})

    if response.status_code == 200:
        tasks = response.json()  # Получаем список задач

        # Находим задачу с нужным name
        for task in tasks:
            if task.get("name") == "Documents Verification":
                task_id = task.get("id")
                
                # Получаем детали задачи
                task_details_response = requests.get(f"http://127.0.0.1:8000/api/task/{task_id}")
                
                if task_details_response.status_code == 200:
                    task_details = task_details_response.json()

                    # Проверяем, есть ли sourceProcessId и совпадает ли он с переданным process_instance_id
                    source_process_id = task_details.get("sourceProcessId", {}).get("value")
                    
                    if source_process_id == process_instance_id:
                        return Response({
                            "message": "Задача найдена!",
                            "task_id": task_id,
                            "process_instance_id": process_instance_id
                        }, status=200)
                    else:
                        return Response({
                            "message": "SourceProcessId не совпадает с переданным processInstanceId"
                        }, status=400)
                else:
                    return Response({
                        "message": "Ошибка при получении деталей задачи",
                        "error": task_details_response.json()
                    }, status=task_details_response.status_code)
        
        return Response({"message": "Задача 'Documents Verification' не найдена"}, status=404)

    return Response({
        "message": "Ошибка при получении списка задач",
        "error": response.json()
    }, status=response.status_code)
    
@api_view(["GET"])
def check_provide_comments_task(request, process_instance_id):
    user_id = request.query_params.get("user_id", "DeanManager")  # Получаем user_id из параметров запроса
    response = requests.get(f"http://localhost:8000/api/tasks/", params={"user_id": user_id})

    if response.status_code == 200:
        tasks = response.json()  # Получаем список задач

        # Находим задачу с нужным name
        for task in tasks:
            if task.get("name") == "Provide comments":
                task_id = task.get("id")

                # Получаем детали задачи
                task_details_response = requests.get(f"http://127.0.0.1:8000/api/task/{task_id}")

                if task_details_response.status_code == 200:
                    task_details = task_details_response.json()

                    # Проверяем, есть ли sourceProcessId и совпадает ли он с переданным process_instance_id
                    source_process_id = task_details.get("sourceProcessId", {}).get("value")

                    if source_process_id == process_instance_id:
                        return Response({
                            "message": "Задача 'Provide comments' найдена!",
                            "task_id": task_id,
                            "process_instance_id": process_instance_id
                        }, status=200)
                    else:
                        return Response({
                            "message": "SourceProcessId не совпадает с переданным processInstanceId"
                        }, status=400)
                else:
                    return Response({
                        "message": "Ошибка при получении деталей задачи",
                        "error": task_details_response.json()
                    }, status=task_details_response.status_code)

        return Response({"message": "Задача 'Provide comments' не найдена"}, status=404)

    return Response({
        "message": "Ошибка при получении списка задач",
        "error": response.json()
    }, status=response.status_code)
    
@api_view(["GET"])
def check_process_status(request, process_instance_id):
    # Запрос к Camunda API для получения информации о процессе
    response = requests.get(f"http://localhost:8080/engine-rest/process-instance/{process_instance_id}")

    if response.status_code == 200:
        process_info = response.json()

        # Проверяем, активен ли процесс
        if process_info.get("ended", False):
            return Response({
                "message": "Процесс завершён",
                "process_instance_id": process_instance_id
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Процесс активен",
                "process_instance_id": process_instance_id
            }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Ошибка при получении статуса процесса",
            "error": response.json()
        }, status=response.status_code)

