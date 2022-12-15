from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def generate_report(filename, string, data1, data2):
    final_list = {}
    pdfmetrics.registerFont(TTFont('Slimamif', 'Slimamif.ttf', 'UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       f'filename={filename}')
    page = canvas.Canvas(response)
    page.setFont('Slimamif', size=24)
    page.drawString(200, 800, f'{string}')
    page.setFont('Slimamif', size=16)
    height = 750
    for i, (name, data) in enumerate(final_list.items(), 1):
        page.drawString(75, height, f'<{i}> {name} - {data[data1]}, '
                                    f'{data[data2]}')
        height -= 25
    page.showPage()
    page.save()
    return response
