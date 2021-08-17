from django.contrib import admin

from .models import House, Board


class HouseAdmin(admin.ModelAdmin):
    fields = ['user', 'address', 'tel', 'post_num']


admin.site.register(House, HouseAdmin)


class BoardAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'content', 'hidden']


admin.site.register(Board, BoardAdmin)
