
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
from .utils import format_key_code


# Create your views here.
def index(request):
	return HttpResponse("Hello, world. Diavaz project!")


def workers_view(request):
	ctx = {
		'workers': Worker.objects.all()
	}
	return render(request, 'workers/workers_list.html', ctx)


def worker_detail(request, key_code):
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


def report_pdf_view(request, key_code, no_paysheet):
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


import pandas as pd
import xlrd

def upload_base_file(request):
	print('===> upload_base_file')
	if request.method == 'POST':
		excel_file = request.FILES["excel_file"]
		print(excel_file)

		data = pd.read_excel(excel_file, index_col=None)
		print(data)

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

		print('==> Terminado la carga de datos!')
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

				print(str(data['ORDEN DE TRABAJO'][i]))
				print(str(data['OBRA'][i]))
				print(int(data['NUMERO DE NÓMINA'][i]))
				print(str(data['CATEGORIA'][i]))
				print(str(data['INICIO DE DIAS REALES'][i])[:10])
				print(str(data['FIN DE DIAS REALES'][i])[:10])
				print(int(data['DIAS DE GUARDIA'][i]))
				print(int(data['FALTAS'][i]))
				print(int(data['DIAS TRABAJADOS'][i]))
				print(int(data['FALTAS'][i]))
				print(float(data['SALARIO DIARIO INTEGRADO'][i]))
				print(float(data['SUELDO PERIODO'][i]))
				print(float(data['SUELDO DESCANSO 1'][i]))
				print(float(data['HORAS EXTRAS DOBLES'][i]))
				print(float(data['HORAS EXTRAS TRIPLES'][i]))

				print('====================================')
				# Reports.objects.create(
				# 	worker = worker_obj,
				# 	work_order = str(data['ORDEN DE TRABAJO'][i]),
				# 	obra = str(data['OBRA'][i]),
				# 	no_paysheet = int(data['NUMERO DE NÓMINA'][i]),
				# 	category = str(data['CATEGORIA'][i]),
				# 	init_period = str(data['INICIO DE DIAS REALES'][i])[:10],
				# 	end_period = str(data['FIN DE DIAS REALES'][i])[:10],
				# 	days_period = int(data['DIAS DE GUARDIA'][i]),
				# 	days_off = int(data['FALTAS'][i]),
				# 	days_working = int(data['DIAS TRABAJADOS'][i]),
				# 	days_lack = int(data['FALTAS'][i]),
				# 	daily_salary = float(data['SALARIO DIARIO INTEGRADO'][i]),
				# 	period_salary = float(data['SUELDO PERIODO'][i]),
				# 	salary_break_1 = float(data['SUELDO DESCANSO 1'][i]),
				# 	salary_break_2 = float(data['HORAS EXTRAS DOBLES'][i]),
				# 	adv_salary_break = float(data['HORAS EXTRAS TRIPLES'][i]),
				# )

		print('==> Terminado la carga de datos!')
	return render(request, 'upload/base_file.html', {})