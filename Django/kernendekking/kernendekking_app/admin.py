from django.contrib import admin
from .models import Level, Measure, Covering
# Register your models here.

class LevelAdmin(admin.ModelAdmin):
    list_display = ('long_name','super_level_short_name','sub_level_name_multiple')

admin.site.register(Level, LevelAdmin)

admin.site.register(Measure)
admin.site.register(Covering)
