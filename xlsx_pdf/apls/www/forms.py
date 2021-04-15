# -*- coding: utf-8 -*-
from django import forms

from .models import BaseFile


class BaseFileForm(forms.ModelForm):
	class Meta:
		model = BaseFile
		exclude = []