from django.http import HttpResponse
from django.shortcuts import render
from .models import Patient
from datetime import date
from django.db.models import F, ExpressionWrapper, IntegerField, Case, When, Value
from django.db.models.functions import Now, ExtractYear, ExtractMonth, ExtractDay
from django.db.models.functions import TruncDate
# Create your views here.
def patient_list(request):
    return render(request, 'patient/patient_list.html') 

def patient_create(request):
    if request.method == "POST":
        try:
            fields = ['first_name', 'last_name', 'gender', 'date_of_birth','phone_number', 'email', 'address']
            patient_data = {field: request.POST.get(field) for field in fields}
            
            patient = Patient(**patient_data)
            patient.save()
            
            return HttpResponse("success", status=200)
        except Exception as ex:
            return HttpResponse(f"error: {str(ex)}", status=500)
def patient_update(request):
    patient_id = request.POST.get('id')
    try:
        patient = Patient.objects.get(pk=patient_id)
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth','phone_number', 'email', 'address']
        for field in fields:
            setattr(patient, field, request.POST.get(field))
        patient.save()
        return HttpResponse("success", status=200)
    except Patient.DoesNotExist:
        return HttpResponse("Patient not found", status=404)
    except Exception as ex:
        return HttpResponse(f"error: {str(ex)}", status=500)
def home(request):
    patients=Patient.objects.all()
    return render(request,"patient/home.html",context={'patients':patients})    