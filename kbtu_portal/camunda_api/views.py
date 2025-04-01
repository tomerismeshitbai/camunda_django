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

       
        camunda_url = f"http://localhost:8080/engine-rest/user/{username}/profile"
        response = requests.get(camunda_url)

        if response.status_code != 200:
            return Response({"error": "User not found in Camunda"}, status=status.HTTP_404_NOT_FOUND)

       
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
            student_data = None 
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
        return Response({"message": "Задача завершена!"})
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