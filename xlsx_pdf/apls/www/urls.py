from django.urls import path

from . import views

app_name = 'site'

urlpatterns = [
	path('', views.index, name='index'),
	path('adm/trabajadores/', views.workers_view, name='workers_view'),	
	path('adm/trabajador/<str:key_code>/', views.worker_detail, name='worker_detail'),
	# Upload excel files
	path('adm/upload_base_file/', views.upload_base_file, name='upload_base_file'),
	path('adm/upload_report_file/', views.upload_report_file, name='upload_report_file'),
	# View PDF data
	path('adm/report_pdf/<str:key_code>/<str:no_paysheet>/', views.report_pdf_view, name='report_pdf_view'),
	path('view_pdf/', views.view_pdf, name='view_pdf'),
	path('render_pdf_view/', views.render_pdf_view, name='render_pdf_view'),
]