# -*- coding: utf-8 -*-
''' Utils functions '''

import math

lst_zero = {
	5: '00000',	
	4: '0000',	
	3: '000',	
	2: '00',	
	1: '0',
	0: ''
}

def format_key_code(value):
	str_value = str(value)
	return '%s%s' % (lst_zero[6 - len(str_value)], str_value)


def remove_zeros(value):
	return value.replace('.0', '') if '.0' in value else value

def nan_to_int(value):
	return 0 if math.isnan(value) else int(value)

def nan_to_dec(value):
	return 0.0 if math.isnan(value) else float(value)

def nan_to_none(value):
	return None if str(value) == 'nan' else remove_zeros(str(value))


# Other utils
def nan_to_sex(value):
	return 'I' if str(value) == 'nan' else str(value)

def nan_to_marital(value):
	return 'S' if str(value) == 'nan' else str(value)
