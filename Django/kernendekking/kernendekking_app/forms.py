from django import forms
from kernendekking_app import models

class CoveringForm(forms.Form):
	covering_level = forms.ModelChoiceField(label='Dekkende niveau', queryset=models.Level.objects.all())
	covered_level = forms.ModelChoiceField(label='Gedekte niveau', queryset=models.Level.objects.all())
	nature = forms.CharField(label='Aard', max_length=63)
	description = forms.CharField(label='Beschrijving', max_length=1023)
	measure = forms.ModelChoiceField(label='Mate', queryset=models.Measure.objects.all())