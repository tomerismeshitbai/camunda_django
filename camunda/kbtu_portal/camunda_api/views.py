import requests
import base64
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser

# URL Camunda
CAMUNDA_BASE_URL = "http://localhost:8080/engine-rest"

@api_view(["POST"])
def start_process(request):
    """
    Запускает процесс Process_student в Camunda 7.
    Принимает student_id в теле запроса.
    """
    student_id = request.data.get("student_id", "unknown")

    data = {
        "variables": {
            "student_id": {"value": student_id, "type": "String"}
        }
    }

    response = requests.post(f"{CAMUNDA_BASE_URL}/process-definition/key/Process_student/start", json=data)

    if response.status_code == 200:
        return Response({"message": "Процесс запущен!", "processInstanceId": response.json().get("id")})
    
    return Response(response.json(), status=response.status_code)


@api_view(["POST"])
def upload_task_file(request, task_id):
    """
    Загружает файл в Camunda в качестве переменной задачи (Base64-кодирование).
    """
    parser_classes = [MultiPartParser]

    file = request.FILES.get("file")
    if not file:
        return Response({"error": "Файл не передан"}, status=400)

    # Кодируем файл в Base64
    encoded_file = base64.b64encode(file.read()).decode("utf-8")

    data = {
        "value": encoded_file,
        "type": "File",
        "valueInfo": {
            "filename": file.name,
            "mimetype": file.content_type
        }
    }

    response = requests.put(
        f"{CAMUNDA_BASE_URL}/task/{task_id}/variables/documentData",
        json=data
    )

    if response.status_code in [204, 200]:
        return Response({"message": "Файл успешно загружен!"})
    
    return Response(response.json(), status=response.status_code)


@api_view(["GET"])
def view_task_file(request, task_id):
    """
    Просмотр файла, связанного с задачей Camunda, в браузере.
    """
    response = requests.get(f"{CAMUNDA_BASE_URL}/task/{task_id}/variables/documentData")

    if response.status_code == 200:
        data = response.json()
        encoded_file = data.get("value")
        filename = data.get("valueInfo", {}).get("filename", "downloaded_file")
        content_type = data.get("valueInfo", {}).get("mimetype", "application/octet-stream")

        # Декодируем Base64 обратно в файл
        file_content = base64.b64decode(encoded_file)

        # Определяем, нужно ли показывать файл в браузере или скачивать
        inline_types = ["pdf", "image", "text"]
        if any(t in content_type for t in inline_types):
            return HttpResponse(
                file_content,
                content_type=content_type,
                headers={"Content-Disposition": "inline"}
            )

        # Для остальных типов предлагаем скачивание
        return HttpResponse(
            file_content,
            content_type=content_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    
    return Response({"error": "Файл не найден"}, status=404)
