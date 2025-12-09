from django.http import HttpResponseForbidden
import ip_tracking.models


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the real IP (even behind proxy later)
        ip = request.META.get('REMOTE_ADDR') or '0.0.0.0'

        # TASK 1: Block if IP is in BlockedIP table
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied – Your IP is blocked")

        # TASK 0: Normal logging
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path
        )

        # Continue to the real view
        response = self.get_response(request)
        return response