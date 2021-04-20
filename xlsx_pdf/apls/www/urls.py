from django.urls import path

from . import views

app_name = 'site'

urlpatterns = [
	path('', views.index, name='index'),
	path('adm/trabajadores/', views.workers_view, name='workers_view'),
	path('adm/trabajador/<str:key_code>/', views.adm_worker_detail, name='adm_worker_detail'),
	path('adm/reportes/', views.reports_view, name='reports_view'),
	path('trabajador/<uuid:id_uuid>/', views.worker_detail, name='worker_detail'),
	path('test_send_mail/<uuid:id_uuid>/', views.send_mail, name='send_mail'),
	path('test_send_mail/all/', views.send_mail_all, name='send_mail_all'),
	# Upload excel files
	path('adm/upload_base_file/', views.upload_base_file, name='upload_base_file'),
	path('adm/upload_report_file/', views.upload_report_file, name='upload_report_file'),
	# View PDF data
	path('adm/report_pdf/<str:key_code>/<str:no_paysheet>/', views.adm_report_pdf_view, name='adm_report_pdf_view'),
	path('trabajador/rpt_pdf/<str:key_code>/<uuid:id_uuid>/', views.report_pdf_view, name='report_pdf_view'),
	path('view_pdf/', views.view_pdf, name='view_pdf'),
	path('render_pdf_view/', views.render_pdf_view, name='render_pdf_view'),
	# Example mailing
	path('adm/mailing/<uuid:id_uuid>/', views.example_mail, name='example_mail'),
]