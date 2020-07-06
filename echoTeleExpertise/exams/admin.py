from django.contrib import admin
from .models import Request, Document

# This class is used to customize the Requests display in the Admin Panel:
class   RequestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'patient_id', 'doctor_id', 'expert_id', 'is_close')
    list_display_links = ('subject', 'patient_id')
    list_filter = ('is_close', 'is_incomplete', 'is_urgent')
    search_fields = ('patient_id', 'doctor_id', 'expert_id')
    list_per_page = 10

# This class is used to customize the Documents display in the Admin Panel:
class   DocumentAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'file')
    search_fields = ('request_id', 'file')
    list_per_page = 10

# Make the Requests & Documents visible in the Admin Panel
admin.site.register(Request, RequestAdmin)
admin.site.register(Document, DocumentAdmin)