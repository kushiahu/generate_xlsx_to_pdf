

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


def nan_to_dec(value):
	return 0.0 if math.isnan(value) else float(value)