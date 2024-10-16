from django.contrib import admin

# Register your models here.
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "domain",
        "comment",
    ]
    empty_value_display = ""
