from django.contrib import admin
from .models import ServiceType, ServiceInstance, Discount, Booking

admin.site.register(ServiceType)
admin.site.register(ServiceInstance)
admin.site.register(Discount)
admin.site.register(Booking)