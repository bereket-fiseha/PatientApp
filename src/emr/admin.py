from django.contrib import admin

# Register your models here.

from .models import Patient,Doctor,MedicalRecord, VitalSign

admin.site.register(Patient)

admin.site.register(Doctor)


admin.site.register(MedicalRecord)

admin.site.register(VitalSign)