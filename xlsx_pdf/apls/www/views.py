
# Django
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render

# Thirds
from django_xhtml2pdf.utils import generate_pdf
from xhtml2pdf import pisa


# Create your views here.
def index(request):
	return HttpResponse("Hello, world. Diavaz project!")


# PDF Views
def view_pdf(response):
	resp = HttpResponse(content_type='application/pdf')
	worker = {
		'name': 'Josué',
		'last_name': 'Tamayo',
	}
	result = generate_pdf('pdf/my_template.html', file_object=resp, context=worker)
	return result



def link_callback(uri, rel):
	"""
	Convert HTML URIs to absolute system paths so xhtml2pdf can access those
	resources
	"""
	result = finders.find(uri)
	if result:
		if not isinstance(result, (list, tuple)):
			result = [result]
		result = list(os.path.realpath(path) for path in result)
		path=result[0]
	else:
		sUrl = settings.STATIC_URL        # Typically /static/
		sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
		mUrl = settings.MEDIA_URL         # Typically /media/
		mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

		if uri.startswith(mUrl):
			path = os.path.join(mRoot, uri.replace(mUrl, ""))
		elif uri.startswith(sUrl):
			path = os.path.join(sRoot, uri.replace(sUrl, ""))
		else:
		        return uri

	# make sure that file exists
	if not os.path.isfile(path):
		raise Exception(
			'media URI must start with %s or %s' % (sUrl, mUrl)
		)
	return path


def render_pdf_view(request):
	template_path = 'pdf/base_pdf.html'
	context = {'patronal': 'A1132476018'}
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	#response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

	# create a pdf
	pisa_status = pisa.CreatePDF(
		html, dest=response, link_callback=link_callback)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response