
# Django
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render

# Thirds
from django_xhtml2pdf.utils import generate_pdf
from xhtml2pdf import pisa

# Models
from .models import Worker, Reports
from .forms import BaseFileForm
from .utils import format_key_code, nan_to_dec


# Create your views here.
def index(request):
	ctx = {
		'workers': Worker.objects.filter(reports__in=Reports.objects.all()).order_by('key_code').distinct()[:16]
	}
	return render(request, 'site/index.html', ctx)


def workers_view(request):
	# Worker.objects.all()
	ctx = {
		'workers': Worker.objects.filter(reports__in=Reports.objects.all()).distinct()
	}
	return render(request, 'workers/workers_list.html', ctx)


def adm_worker_detail(request, key_code):
	try:
		worker_obj = Worker.objects.get(key_code=key_code)
		report_lst = worker_obj.reports.all()
		#print(report_lst)
		ctx = {
			'worker_obj': worker_obj,
			'report_lst': report_lst,
		}
	except Exception as e:
		raise
	return render(request, 'workers/workers_detail.html', ctx)

def reports_view(request):
	ctx = {
		'reports': Reports.objects.all()
	}
	return render(request, 'workers/reports_list.html', ctx)


def worker_detail(request, id_uuid):
	try:
		worker_obj = Worker.objects.get(id_uuid=id_uuid)
		report_lst = worker_obj.reports.all()
		ctx = {
			'worker_obj': worker_obj,
			'report_lst': report_lst,
		}
	except Exception as e:
		raise
	return render(request, 'workers/workers_detail.html', ctx)


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
	pisa_status = pisa.CreatePDF(
		html, dest=response, link_callback=link_callback)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response


import pandas as pd
import xlrd

def upload_base_file(request):
	'''
		Upload the workers general data
	'''
	print('===> upload_base_file')
	if request.method == 'POST':
		excel_file = request.FILES["excel_file"]

		data = pd.read_excel(excel_file, index_col=None)

		cont = 0

		for i in data.index:
			key_code = format_key_code(data['id_empleado'][i])
			if not Worker.objects.filter(key_code=key_code).exists():
				print('Save: ' + str(key_code))
				Worker.objects.create(
					key_code = key_code,
					name = str(data['nombre'][i]),
					first_name = str(data['a_paterno'][i]),
					last_name = str(data['a_materno'][i]),
					sex = str(data['sexo'][i]),
					marital_status = str(data['estado_civil'][i]),
					age = str(data['edad'][i]),
					rfc = str(data['rfc'][i]),
					curp = str(data['curp'][i]),
					imss = str(data['imss'][i]),
					afore = str(data['afore'][i]),
					infonavit = str(data['infonavit'][i]),
					email = str(data['correo'][i])
				)
				cont += 1

		print('==> Terminado la carga de datos!')
		print('==> Se ha añadido %s nuevos trabajadores' % str(cont))
	return render(request, 'upload/base_file.html', {})

import math
def upload_report_file(request):
	print('===> upload_report_file')
	if request.method == 'POST':
		excel_file = request.FILES["excel_file"]
		data = pd.read_excel(excel_file, index_col=None)

		for i in data.index:
			key_code = format_key_code(data['FICHA'][i])
			worker_obj = Worker.objects.get(key_code=key_code)

			if (not math.isnan(data['NUMERO DE NÓMINA'][i]) and 
				not worker_obj.reports.filter(no_paysheet=int(data['NUMERO DE NÓMINA'][i])).exists()):
				print('save: ' + key_code)
				Reports.objects.create(
					worker = worker_obj,
					work_order = str(data['ORDEN DE TRABAJO'][i]),
					obra = str(data['OBRA'][i]),
					no_paysheet = int(data['NUMERO DE NÓMINA'][i]),
					category = str(data['CATEGORIA'][i]),
					init_period = str(data['INICIO DE DIAS REALES'][i])[:10],
					end_period = str(data['FIN DE DIAS REALES'][i])[:10],
					days_period = int(data['DIAS DE GUARDIA'][i]),
					days_off = int(data['FALTAS'][i]),
					days_working = int(data['DIAS TRABAJADOS'][i]),
					days_lack = int(data['FALTAS'][i]),
					daily_salary = nan_to_dec(data['SALARIO DIARIO INTEGRADO'][i]),
					period_salary = nan_to_dec(data['SUELDO PERIODO'][i]),
					salary_break_1 = nan_to_dec(data['SUELDO DESCANSO 1'][i]),
					salary_break_2 = nan_to_dec(data['HORAS EXTRAS DOBLES'][i]),
					adv_salary_break = nan_to_dec(data['HORAS EXTRAS TRIPLES'][i]),
				)

		print('==> Terminado la carga de datos!')
	return render(request, 'upload/base_file.html', {})