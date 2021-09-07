from django.contrib import admin
from .models import FitnessSpec, FitnessActivate


class FitnessSpecAdmin(admin.ModelAdmin):
    fields = ['spec', 'icon', 'calorie']


admin.site.register(FitnessSpec, FitnessSpecAdmin)


class FitnessActivateAdmin(admin.ModelAdmin):
    fields = ['user', 'fitness', 'minute']
    # fields = ['__all__']


admin.site.register(FitnessActivate, FitnessActivateAdmin)
