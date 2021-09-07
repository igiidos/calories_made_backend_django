from django.contrib import admin

from accounts.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'sex', 'birth', 'height', 'weight']


admin.site.register(Profile, ProfileAdmin)
