from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 


def render_to_pdf(request, pk):
    app = InternshipApp.objects.get(id=pk)
    marks = Marks.objects.filter(intern= app.applicant)
    # Get the HTML template
    template = get_template('Certificate.html')
    context = {'marks': marks}  # Add your context data

    # Render the template with the context
    html = template.render(context)

    # Create a PDF file using xhtml2pdf
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    # Check if PDF generation was successful
    if not pdf.err:
        # Set the appropriate response headers for PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Certificate.pdf"'

        # Write the PDF file to the response
        response.write(result.getvalue())

        return response

    # Return an error response if PDF generation failed
    return HttpResponse('Error generating PDF', status=500)
