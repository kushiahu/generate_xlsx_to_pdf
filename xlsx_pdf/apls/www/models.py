# -*- coding: utf-8 -*-
'''Users test employes'''

# Django
import uuid
from django.db import models
from django.urls import reverse


# Create your models here.
class Worker(models.Model):

	SEX = (
		('F', 'Femenino'),
		('M', 'Masculino'),
	)

	MARITAL = (
		('C', 'Casado(a)'),
		('S', 'Soltero(a)'),
	)

	STATUS = (
		('A', 'Activo(a)'),
		('E', '--------'),
		('I', 'Inactivo(a)'),
	)

	id_uuid = models.CharField(default=uuid.uuid4, max_length=36, editable=False)
	key_code = models.CharField(max_length=6, unique=True)

	name = models.CharField(max_length=64)
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64, null=True, blank=True)
	sex = models.CharField(max_length=1, choices=SEX, null=True, blank=True)
	marital_status = models.CharField(max_length=1, choices=MARITAL, default='S', null=True, blank=True)
	age = models.PositiveIntegerField(null=True, blank=True)

	status = models.CharField(max_length=1, choices=STATUS, null=True, blank=True)
	rfc = models.CharField(max_length=13, null=True, blank=True)
	curp = models.CharField(max_length=18, null=True, blank=True)
	imss = models.CharField(max_length=11, null=True, blank=True)
	afore = models.CharField(max_length=24, null=True, blank=True)
	infonavit = models.CharField(max_length=24, null=True, blank=True)

	email = models.EmailField(null=True, blank=True)

	class Meta:
		verbose_name = "Worker"
		verbose_name_plural = "Workers"

	@property
	def full_name(self):
		return '%s %s %s' % (self.name, self.first_name, self.last_name)

	@property
	def imss_cln(self):
		return self.imss if self.imss else '---'

	@property
	def afore_cln(self):
		return self.afore if self.afore else '---'

	@property
	def infonavit_cln(self):
		return self.infonavit if self.infonavit else '---'

	@property
	def email_cln(self):
		return self.email if self.email else '---'

	def get_absolute_url(self):		
		return reverse('site:worker_detail', args=(self.id_uuid,))

	def __str__(self):
		return self.key_code


class Reports(models.Model):

	id_uuid = models.CharField(default=uuid.uuid4, max_length=36, editable=False)
	worker = models.ForeignKey(
		Worker, related_name='reports',
		related_query_name='reports',
		on_delete=models.CASCADE)

	work_order = models.CharField(max_length=64)
	obra = models.CharField(max_length=32)
	no_paysheet = models.PositiveIntegerField()		# Numero de nomina

	category = models.CharField(max_length=120)

	init_period = models.CharField(max_length=10)
	end_period = models.CharField(max_length=10)
	days_period = models.PositiveIntegerField()		# Días periodo
	days_off = models.PositiveIntegerField() 		# Días de descanso
	days_working = models.PositiveIntegerField() 	# Días reales trabajados
	days_lack = models.PositiveIntegerField() 		# Faltas

	daily_salary = models.DecimalField(max_digits=12, decimal_places=2)

	# Perceptions
	period_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	salary_break_1 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	salary_break_2 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	adv_salary_break = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	extra_double = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	extra_triple = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	seventh_day = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	prm_dominical = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	salary_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	period_vacancy = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	prm_vacations = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	coupons = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)				# Vales de despensa
	award_assists = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)			# Premio por asistencia
	award_puntuality = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)		# Premio de puntualidad
	others_inf = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)				# Otros (INF)
	subsidy = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)				# Subsidio para el empleo
	favor_infonavit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)		# Devolución infonavit a favor
	total_perceptions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)		# TOTAL de percepciones

	# Deductions
	isr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	retn_imss = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	amr_infonavit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	dct_loan = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	alimony_01 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	alimony_02 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	various_discounts = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)		# Descuentos varios
	others_discounts = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)		# Otros descuentos
	break_discounts = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)		# Descuento anticipo descanso
	special_discounts = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)		# Descuento especial
	debts = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)					# Adeudo empresa amort
	total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)		# TOTAL deducciones

	# Totals
	total_receive = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	total_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	total_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

	class Meta:
		verbose_name = "Report"
		verbose_name_plural = "Reports"

	@property
	def period_payment(self):
		return '%s - %s' % (self.init_period, self.end_period)

	def get_url_report_pdf(self):		
		return '/trabajador/rpt_pdf/%s/%s/' % (self.worker.key_code, self.id_uuid)

	def __str__(self):
		return str(self.category)




# files
class BaseFile(models.Model):
	file = models.FileField(upload_to='excel_files/')
	created = models.DateTimeField(auto_now_add=True)