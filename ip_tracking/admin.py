from django.contrib import admin

from .app.models import BlockedIP, RequestLog


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "timestamp", "path", "country", "city")
    search_fields = ("ip_address", "country", "city", "path")
    list_filter = ("country", "city", "timestamp")
    ordering = ("-timestamp",)

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ("ip_address",)
    search_fields = ("ip_address",)
