from django.contrib import admin
from .models import Click


class ClickAdmin(admin.ModelAdmin):
    list_display = ['address', 'browser', 'user', 'time']


admin.site.register(Click, ClickAdmin)
