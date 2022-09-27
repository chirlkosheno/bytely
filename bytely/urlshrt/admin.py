from django.contrib import admin
from .models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'full_url')
    search_field = ('short_url, full_url')
