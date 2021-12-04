from django.http import HttpResponse

from productos.models import Provider, Ticket

# encoding: utf-8
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



def render_pdf(url_template, contexto={}):
    template = get_template(url_template)
    html= template.render(contexto)
    result= BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue() , content_type= "application/pdf")
    return None















#
# def print_report(self, pk=None):
#     import io
#     from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
#     from reportlab.lib.styles import getSampleStyleSheet
#     from reportlab.lib import colors
#     from reportlab.lib.pagesizes import letter
#     from reportlab.platypus import Table
#
#     response = HttpResponse(content_type='application/pdf')
#     buff = io.BytesIO()
#     doc = SimpleDocTemplate(buff,
#                             pagesize=letter,
#                             rightMargin=40,
#                             leftMargin=40,
#                             topMargin=60,
#                             bottomMargin=18,
#                             )
#     productos = []
#     styles = getSampleStyleSheet()
#     header = Paragraph("Listado de productos", styles['Heading1'])
#     productos.append(header)
#     headings = ('Id', 'Descrición', 'Activo', 'Creación')
#     if not pk:
#         todascategorias = [(p.id, p.descripcion, p.activo, p.creado)
#                            for p in Provider.objects.all().order_by('pk')]
#     else:
#         todascategorias = [(p.id, p.descripcion, p.activo, p.creado)
#                            for p in Categoria.objects.filter(id=pk)]
#     t = Table([headings] + todascategorias)
#     t.setStyle(TableStyle(
#         [
#             ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
#             ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
#         ]
#     ))
#
#     categorias.append(t)
#     doc.build(categorias)
#     response.write(buff.getvalue())
#     buff.close()
#     return response