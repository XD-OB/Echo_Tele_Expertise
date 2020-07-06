from django.contrib import admin
from .models import Patient, Relation

# This class is used to customize the Patients display in the Admin Panel:
class   PatientAdmin(admin.ModelAdmin):
    list_display = ('cin', 'last_name', 'first_name')
    list_display_links = ('cin', )
    list_filter = ('gender', )
    search_fields = ('last_name', 'first_name', 'cin')
    list_per_page = 10

# This class is used to customize the Realation between Doctor & Patient display in the Admin Panel:
class   RelationAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'doctor_id')
    list_display_links = ('patient_id', )
    search_fields = ('patient_id', 'doctor_id')
    list_per_page = 10

admin.site.register(Patient, PatientAdmin)
admin.site.register(Relation, RelationAdmin)