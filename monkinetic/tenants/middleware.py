from django.http import HttpResponseForbidden
from .models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.get_host())
        domain = request.get_host().split(":")[0]
        print(f"Tenant Domain {domain}")
        try:
            tenant = Tenant.objects.get(domain=domain)
            request.tenant = tenant
        except Tenant.DoesNotExist:
            request.tenant = None

        response = self.get_response(request)
        return response
