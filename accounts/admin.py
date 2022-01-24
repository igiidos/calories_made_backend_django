from django.contrib import admin

from accounts.models import Profile, Token


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'sex', 'birth', 'height', 'weight']


admin.site.register(Profile, ProfileAdmin)


class TokenAdmin(admin.ModelAdmin):
    fields = ['key', 'user']

admin.site.register(Token, TokenAdmin)
