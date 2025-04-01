from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from .models import CourseRegistrationApplication
from datetime import date
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('times', r'C:\Windows\Fonts\times.ttf'))

def generate_course_registration_pdf(application_id):
    """Генерирует заявление в PDF."""
    application = CourseRegistrationApplication.objects.get(pk=application_id)
    student = application.student

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Заявление_на_регистрацию_дисциплины_{student.full_name}_{student.kbtu_id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("times", 12)

    # **Шапка заявления**
    p.drawString(width - 250, height - 50, "Декану ШИТиИ")
    p.drawString(width - 250, height - 70, "Иманбаеву А.Ж.")

    # **Данные студента**
    p.drawString(50, height - 100, f"от студента {student.course}г.о.")
    p.drawString(50, height - 120, f"ОП {student.speciality}")
    p.drawString(50, height - 140, f"{student.full_name}")
    p.drawString(50, height - 160, f"Сот. номер: {student.telephone_number}")
    p.drawString(50, height - 180, f"e-mail: {student.email}")

    # **Заголовок заявления**
    p.setFont("times", 14)
    p.drawCentredString(width / 2, height - 220, "ЗАЯВЛЕНИЕ")

    # **Текст**
    p.setFont("times", 12)
    p.drawString(50, height - 250, f"Прошу Вас разрешить мне зарегистрироваться на следующие дисциплины {application.semester} семестра 2024–2025 учебного года:")

    y_position = height - 280
    for idx, course in enumerate(application.courses, start=1):
        course_text = f"{idx}. {course['code']} - {course['name']} ({course['credits_kz']} KZ / {course['credits_ects']} ECTS)"
        if course['retake']:
            course_text += " (Ритейк)"
        p.drawString(50, y_position, course_text)
        y_position -= 20

    # **Дата и подпись**
    p.drawString(50, y_position - 40, f"Дата: {date.today().strftime('%d.%m.%Y')}")
    p.drawString(350, y_position - 40, f"Подпись: _______________ ({student.full_name})")

    p.showPage()
    p.save()
    return response
