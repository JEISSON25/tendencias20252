from django.contrib import admin
from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("fecha_hora", "status", "level", "usuario", "short_message")
    list_filter = ("status", "level", "fecha_hora")
    search_fields = ("message", "usuario__username")
    date_hierarchy = "fecha_hora"
    ordering = ("-fecha_hora",)

    def short_message(self, obj):
        return (obj.message[:75] + "...") if len(obj.message) > 75 else obj.message

    short_message.short_description = "Mensaje"
