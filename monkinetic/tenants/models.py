from django.db import models

app_name = "tenants"


# Create your models here.
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, unique=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.name
