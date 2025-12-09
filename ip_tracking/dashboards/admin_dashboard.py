from django.contrib import admin
from django.urls import path
from django.shortcuts import render
import ip_tracking.models
from django.db.models import Count
from django.utils import timezone
import datetime


def ip_analytics_view(request):
    today = timezone.now().date()

    # Requests per country
    country_data = (
        RequestLog.objects.values("country")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # Requests per city
    city_data = (
        RequestLog.objects.values("city")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # Requests for last 7 days chart
    last_week = today - datetime.timedelta(days=7)
    weekly_data = (
        RequestLog.objects.filter(timestamp__date__gte=last_week)
        .values("timestamp__date")
        .annotate(total=Count("id"))
        .order_by("timestamp__date")
    )

    return render(request, "admin/ip_analytics_dashboard.html", {
        "country_data": country_data,
        "city_data": city_data,
        "weekly_data": weekly_data
    })


class IPAnalyticsDashboard(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ip-analytics/', self.admin_site.admin_view(ip_analytics_view))
        ]
        return custom_urls + urls

from ip_tracking.dashboards.admin_dashboard import IPAnalyticsDashboard
from django.contrib import admin

admin.site.register_view(
    "ip-analytics",
    view=IPAnalyticsDashboard().ip_analytics_view,
    name="IP Analytics Dashboard"
)
