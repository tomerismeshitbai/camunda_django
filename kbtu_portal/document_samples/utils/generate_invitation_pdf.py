from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from document_samples.models import InvitationLetter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('times', r'C:\Windows\Fonts\times.ttf'))

def generate_invitation_pdf(invitation_id):
    """Генерирует PDF-приглашение на практику."""
    invitation = InvitationLetter.objects.get(pk=invitation_id)
    

    # Создание HTTP-ответа с PDF-файлом
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invitation_{invitation.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    # Заголовок
    p.setFont("times", 14)
    p.drawString(240, 800, "ПИСЬМО-ПРИГЛАШЕНИЕ")

    # Тело письма
    p.setFont("times", 12)
    p.drawString(100, 770, f"Полное название организации: {invitation.organization_name}")
    p.drawString(100, 750, "согласны принять на производственную практику в соответствии с ")
    p.drawString(100, 730, f"учебной программой студента  {invitation.student.course} года обучения по образовательной программе")
    p.drawString(100, 710, f"{invitation.student.speciality} ШИТиИ")
    p.drawString(100, 690, f"{invitation.student.last_name} {invitation.student.first_name} {invitation.student.middle_name}")
    p.drawString(100, 670, f"в период с {invitation.start_date} по {invitation.end_date}")

    # Подпись руководителя
    p.drawString(300, 320, "МП                    Руководитель практики от предприятия")
    p.drawString(300, 300, f"{invitation.supervisor_name}")
    p.drawString(300, 280, f"{invitation.supervisor_position}")
    p.drawString(300, 260, f"«     » _________________ {invitation.current_year} г.")

    p.showPage()
    p.save()
    return response
