# -*- coding: utf-8 -*-
''' Render data to PDF Views '''

# Django
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template

# Thirds
from django_xhtml2pdf.utils import generate_pdf
from xhtml2pdf import pisa

# Models
from apls.www.models import Worker


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
	lvl = {}
	ctx = {'patronal': 'A1132476018'}
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	#response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(ctx)

	# create a pdf
	pisa_status = pisa.CreatePDF(
		html, dest=response, link_callback=link_callback)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response


def adm_report_pdf_view(request, key_code, no_paysheet):
	template_path = 'pdf/base_pdf.html'
	ctx = None
	try:
		worker_obj = Worker.objects.get(key_code=key_code)
		report_obj = worker_obj.reports.get(no_paysheet=no_paysheet)
		ctx = {
			'worker_obj': worker_obj,
			'report_obj': report_obj,
		}
	except Exception as e:
		raise
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	#response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(ctx)

	# create a pdf
	pisa_status = pisa.CreatePDF(
		html, dest=response, link_callback=link_callback)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response


def report_pdf_view(request, key_code, id_uuid):
	template_path = 'pdf/base_pdf.html'
	# ?print=True
	can_print = request.GET.get('print')
	name_pdf = 'report'
	ctx = None
	try:
		worker_obj = Worker.objects.get(key_code=key_code)
		report_obj = worker_obj.reports.get(id_uuid=id_uuid)
		ctx = {
			'worker_obj': worker_obj,
			'report_obj': report_obj,
		}
		name_pdf = '%s - nómina_%s' % (worker_obj.key_code, report_obj.no_paysheet)
	except Exception as e:
		raise
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	if can_print:
		response['Content-Disposition'] = 'attachment; filename="' + name_pdf + '.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(ctx)

	# create a pdf
	pisa_status = pisa.CreatePDF(html, dest=response)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response