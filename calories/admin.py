from django.contrib import admin
from .models import FitnessSpec, FitnessActivate, FoodSpec, IncomeFoods


class FitnessSpecAdmin(admin.ModelAdmin):
    fields = ['spec', 'icon', 'calorie']


admin.site.register(FitnessSpec, FitnessSpecAdmin)


class FitnessActivateAdmin(admin.ModelAdmin):
    fields = ['user', 'fitness', 'minute']
    # fields = ['__all__']


admin.site.register(FitnessActivate, FitnessActivateAdmin)


class FoodSpecAdmin(admin.ModelAdmin):
    fields = ['spec', 'icon', 'calorie']


admin.site.register(FoodSpec, FoodSpecAdmin)


class IncomeFoodsAdmin(admin.ModelAdmin):
    fields = ['user', 'food', 'portion', 'income_calories']


admin.site.register(IncomeFoods, IncomeFoodsAdmin)
