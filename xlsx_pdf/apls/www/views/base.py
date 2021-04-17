# -*- coding: utf-8 -*-
''' Workers and Reports View '''

# Django
from django.shortcuts import render

# Models
from apls.www.models import Worker, Reports


# Create your views here.
def index(request):
	ctx = {
		'workers': Worker.objects.filter(reports__in=Reports.objects.all()).order_by('key_code').distinct()[:16],
		'without_email': Worker.objects.filter(email=None),
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