from django.urls import path

from . import views

app_name = 'site'

urlpatterns = [
	path('', views.index, name='index'),
	path('view_pdf/', views.view_pdf, name='view_pdf'),
	path('render_pdf_view/', views.render_pdf_view, name='render_pdf_view'),
]