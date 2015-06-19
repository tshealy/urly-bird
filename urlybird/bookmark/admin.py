from django.contrib import admin
from .models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['long', 'short', 'created', 'edited', 'title', 'description']


admin.site.register(Bookmark, BookmarkAdmin)