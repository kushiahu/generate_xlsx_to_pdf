# -*- coding: utf-8 -*-
''' Send Emails to Users'''

# Django
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Model
from apls.www.models import Worker, Reports


# Send email's functions
# host = request.META['HTTP_HOST']
def send_link(worker_id, host='localhost:8000'):
	# Create Activation user
	print('--- send_link ---')
	try:
		worker_obj = Worker.objects.get(id_uuid=worker_id)

		ctx = {
			'username': worker_obj.full_name,
			'report_url': 'http://%s%s' % (host, worker_obj.get_absolute_url()),
		}

		data_plain = {
			'username': worker_obj.full_name,
			'email': worker_obj.email,
			'report_url': 'http://%s%s' % (host, worker_obj.get_absolute_url())
		}

		msg_plain = render_to_string('_mailings/report_link.txt', data_plain)
		msg_html = render_to_string('_mailings/report_link.html', ctx)

		subject = 'Lista de Nóminas de DITRA'
		message = msg_plain
		email_from = 'DITRA <%s>' % settings.EMAIL_HOST_USER
		recipient_list = [worker_obj.email]
		send_mail(
			subject, message,
			email_from, recipient_list,
			fail_silently=False,
			html_message=msg_html
		)
	except Exception as e:
		print(e)



def send_link_all(host='localhost:8000'):
	# Create Activation user
	print('--- send_link_all ---')
	
	worker_lst = Worker.objects.filter(
					reports__in=Reports.objects.all()
				).order_by('key_code').distinct()[:4]

	for worker_obj in worker_lst:
		try:

			ctx = {
				'username': worker_obj.full_name,
				'report_url': 'http://%s%s' % (host, worker_obj.get_absolute_url()),
			}

			data_plain = {
				'username': worker_obj.full_name,
				'email': worker_obj.email,
				'report_url': 'http://%s%s' % (host, worker_obj.get_absolute_url())
			}

			msg_plain = render_to_string('_mailings/report_link.txt', data_plain)
			msg_html = render_to_string('_mailings/report_link.html', ctx)

			subject = 'Lista de Nóminas de DITRA'
			message = msg_plain
			email_from = 'DITRA <%s>' % settings.EMAIL_HOST_USER
			#recipient_list = [worker_obj.email]
			recipient_list = [
				'tamayo.josue@gmail.com',
				'pp.tamayo@hotmail.com',
				'robero_porto@diavaz.com',
				'claudia_lopez@diavaz.com',
				'sandra_reyes@diavaz.com',
			]
			send_mail(
				subject, message,
				email_from, recipient_list,
				fail_silently=False,
				html_message=msg_html
			)
		except Exception as e:
			print(e)