from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from kernendekking_app import models
from kernendekking_app.models import Level, Covering, Measure
from kernendekking_app.forms import CoveringForm

# Create your views here.
def levels(request, segments):
    current_level = None
    for level_name in segments.split('/'):
        current_level = models.Level.objects.get(super_level_id=current_level,short_name=level_name)
    return render(request, 'levels.html', {'levels': current_level.sub_level.all, 'current_level': current_level.sub_level_name_multiple, 'segments': segments + '/'})

def levelsTop(request):
    top_level = models.Level.objects.filter(super_level_id=None)
    return render(request, 'levels.html', {'levels': top_level, 'current_level': "", 'segments': ""})

def coverings(request, segments):
    current_level = None
    for level_name in segments.split('/'):
        current_level = models.Level.objects.get(super_level_id=current_level, short_name=level_name)

    coverings = models.Covering.objects.filter(covering_level_id=current_level)
    return render(request, 'coverings.html', {'level': current_level, 'coverings': coverings})
 
def covered(request, segments):
    current_level = None
    for level_name in segments.split('/'):
        current_level = models.Level.objects.get(super_level_id=current_level, short_name=level_name)

    coverings = models.Covering.objects.filter(covered_level_id=current_level)
    return render(request, 'covered.html', {'level': current_level, 'coverings': coverings})

def coveringForm(request):
    if request.method == 'POST':
        form = CoveringForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('/kernendekking/')
    else:
        form = CoveringForm()
    return render(request, 'form.html', {'form': form})