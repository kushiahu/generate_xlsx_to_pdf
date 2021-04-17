# -*- coding: utf-8 -*-
''' Upload Data Excel Views '''

# Django
from django.shortcuts import render

# Third
import pandas as pd

# Models
from apls.www.models import Worker, Reports

# Utils
from apls.www.utils import (
	format_key_code, nan_to_none,
	 nan_to_dec, nan_to_int,
)


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
				print('--> Nombre: ' + str(data['nombre'][i])
				Worker.objects.create(
					key_code = key_code,
					name = str(data['nombre'][i]),
					first_name = str(data['a_paterno'][i]),
					last_name = str(data['a_materno'][i]),
					sex = str(data['sexo'][i]),
					marital_status = str(data['estado_civil'][i]),
					age = nan_to_int(data['edad'][i]),
					rfc = nan_to_none(data['rfc'][i]),
					curp = nan_to_none(data['curp'][i]),
					imss = nan_to_none(data['imss'][i]),
					afore = nan_to_none(data['afore'][i]),
					infonavit = nan_to_none(data['infonavit'][i]),
					email = nan_to_none(data['correo'][i]),
					status = str(data['status'][i]),
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
		print(excel_file)

		data = pd.read_excel(excel_file, index_col=None)

		for i in data.index:
			key_code = format_key_code(data['FICHA'][i])
			try:
				worker_obj = Worker.objects.get(key_code=key_code)				

				if (not math.isnan(data['NUMERO DE NÓMINA'][i]) and 
					not worker_obj.reports.filter(no_paysheet=int(data['NUMERO DE NÓMINA'][i])).exists()):
					print('save: ' + key_code)

					total_perc = (
						nan_to_dec(data['SUELDO PERIODO'][i]) +
						nan_to_dec(data['SUELDO DESCANSO 1'][i]) +
						nan_to_dec(data['SUELDO DESCANSO 1'][i]) +
						nan_to_dec(data['SUELDO PERIODO'][i]) +
						nan_to_dec(data['HORAS EXTRAS DOBLES'][i]) +
						nan_to_dec(data['HORAS EXTRAS TRIPLES'][i]) +
						nan_to_dec(data['SEPTIMO DIA'][i]) +
						nan_to_dec(data['PRIMA DOMINICAL'][i]) +
						nan_to_dec(data['AGUINALDO'][i]) +
						nan_to_dec(data['VACACIONES DEL PERIODO'][i]) +
						nan_to_dec(data['PRIMA VACACIONAL'][i]) +
						nan_to_dec(data['VALES DE DESPENSA'][i]) +
						nan_to_dec(data['PREMIO POR ASISTENCIA'][i]) +
						nan_to_dec(data['PREMIO POR PUNTUALIDAD'][i]) +
						nan_to_dec(data['OTROS (INF)'][i]) +
						nan_to_dec(data['SUBSIDIO PARA EL EMPLEO'][i]) +
						0.0
					)

					total_ded = (
						nan_to_dec(data['ISR NETO'][i]) +
						nan_to_dec(data['TOTAL CUOTA OBRERA IMSS'][i]) +
						nan_to_dec(data['AMORTIZACION INFONAVIT'][i]) +
						nan_to_dec(data['DESCUENTO PRESTAMO A EMPLEADOS'][i]) +
						nan_to_dec(data['PENSION ALIMENTICIA 1'][i]) +
						0.0 +
						nan_to_dec(data['DESCUENTOS VARIOS'][i]) +
						nan_to_dec(data['OTROS DESCUENTOS'][i]) +
						0.0 +
						0.0 +
						nan_to_dec(data['ADEUDO EMPRESA AMORT.'][i])
					)

					total_rec = (
						nan_to_dec(data['TOTAL DE PERCEPCIONES'][i]) -
						nan_to_dec(data['TOTAL DE DEDUCCIONES'][i]) -
						nan_to_dec(data['VALES DE DESPENSA'][i])
					)

					Reports.objects.create(
						worker = worker_obj,
						work_order = str(data['ORDEN DE TRABAJO'][i]),
						obra = str(data['OBRA'][i]),
						no_paysheet = int(data['NUMERO DE NÓMINA'][i]),
						category = str(data['CATEGORIA'][i]),
						init_period = str(data['INICIO DE DIAS REALES'][i])[:10],
						end_period = str(data['FIN DE DIAS REALES'][i])[:10],
						days_period = nan_to_int(data['DIAS REALES'][i]),
						days_off = nan_to_int(data['DIAS DE GUARDIA'][i]) - nan_to_int(data['DIAS REALES'][i]),
						days_working = nan_to_int(data['DIAS TRABAJADOS REALES'][i]),
						days_lack = nan_to_int(data['FALTAS DEL PERIODO'][i]),
						daily_salary = nan_to_dec(data['SALARIO DIARIO INTEGRADO'][i]),
						period_salary = nan_to_dec(data['SUELDO PERIODO'][i]),
						salary_break_1 = nan_to_dec(data['SUELDO DESCANSO 1'][i]),
						salary_break_2 = nan_to_dec(data['SUELDO DESCANSO 1'][i]),		# Por determinar
						adv_salary_break = nan_to_dec(data['SUELDO PERIODO'][i]),		# Por determinar
						extra_double = nan_to_dec(data['HORAS EXTRAS DOBLES'][i]),
						extra_triple = nan_to_dec(data['HORAS EXTRAS TRIPLES'][i]),
						seventh_day = nan_to_dec(data['SEPTIMO DIA'][i]),
						prm_dominical = nan_to_dec(data['PRIMA DOMINICAL'][i]),
						salary_bonus = nan_to_dec(data['AGUINALDO'][i]),
						period_vacancy = nan_to_dec(data['VACACIONES DEL PERIODO'][i]),
						prm_vacations = nan_to_dec(data['PRIMA VACACIONAL'][i]),
						coupons = nan_to_dec(data['VALES DE DESPENSA'][i]),
						award_assists = nan_to_dec(data['PREMIO POR ASISTENCIA'][i]),
						award_puntuality = nan_to_dec(data['PREMIO POR PUNTUALIDAD'][i]),
						others_inf = nan_to_dec(data['OTROS (INF)'][i]),
						subsidy = nan_to_dec(data['SUBSIDIO PARA EL EMPLEO'][i]),
						favor_infonavit = 0.0,											# Falta
						total_perceptions = total_perc,
						isr = nan_to_dec(data['ISR NETO'][i]),
						retn_imss = nan_to_dec(data['TOTAL CUOTA OBRERA IMSS'][i]),
						amr_infonavit = nan_to_dec(data['AMORTIZACION INFONAVIT'][i]),
						dct_loan = nan_to_dec(data['DESCUENTO PRESTAMO A EMPLEADOS'][i]),
						alimony_01 = nan_to_dec(data['PENSION ALIMENTICIA 1'][i]),
						alimony_02 = 0.0,												# Falta
						various_discounts = nan_to_dec(data['DESCUENTOS VARIOS'][i]),
						others_discounts = nan_to_dec(data['OTROS DESCUENTOS'][i]),
						break_discounts = 0.0,											# Falta
						special_discounts = 0.0,										# Falta
						debts = nan_to_dec(data['ADEUDO EMPRESA AMORT.'][i]),
						total_deductions = total_ded,
						total_receive = total_rec,
						total_bonus = nan_to_dec(data['VALES DE DESPENSA'][i]),
						total_pay = total_rec + nan_to_dec(data['VALES DE DESPENSA'][i])
					)

			except Exception as e:
				print('==> (ERROR) apls.www.models.Worker.DoesNotExist: Worker matching query does not exist.')
				print('    --> Ficha %s' % key_code)

		print('==> Terminado la carga de datos!')
	return render(request, 'upload/base_file.html', {})