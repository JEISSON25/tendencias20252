from django.contrib import admin
from .models import GlobalSettings, ServiceType, ServiceInstance, Discount, Booking

admin.site.register(ServiceType)
admin.site.register(ServiceInstance)
admin.site.register(Discount)
admin.site.register(Booking)
admin.site.register(GlobalSettings)