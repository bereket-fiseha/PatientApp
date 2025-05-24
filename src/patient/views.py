from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Patient
from datetime import date
from django.db.models import F, ExpressionWrapper, IntegerField, Case, When, Value
from django.db.models.functions import Now, ExtractYear, ExtractMonth, ExtractDay
from django.db.models.functions import TruncDate
from django.core.mail import send_mail
from django.core.serializers import serialize
# Create your views here.
def patient_list(request):
    return render(request, 'patient/patient_list.html') 

def  patient_get(request,id:int):
    if request.method != "GET":
        return HttpResponse(status=405)
    try:
     todo=Patient.objects.get(pk=id)
    except:
        return HttpResponse(status=500)
    todo_json = serialize('json', [todo,])
    return HttpResponse(todo_json, content_type='application/json',status=200)
    
def patient_save(request):
    if(request.method != "POST"):
        return HttpResponse(status=405)
    if not request.POST.get('id'):
        print("in create")
        return _patient_create(request)
    else:
        print("in update")
        return _patient_update(request)


def _patient_create(request):
    if request.method == "POST":
        try:
            fields = ['first_name', 'last_name', 'gender', 'date_of_birth','phone_number', 'email', 'address']
            patient_data = {field: request.POST.get(field) for field in fields}
            
            patient = Patient(**patient_data)
            patient.save()
            email_sent = send_mail('Patient Registration Notification',
                      'Hi there,\n\You have been registered successfully in our app ,please use the patient portal from now on\n\nRegards,\n',
                        'Bereket Fiseha codigorey111@gmail.com',
                         ['bereketfiseha123@gmail.com'],
                         fail_silently=False,
                              )
            email_status = "success" if email_sent else "failed"
            return JsonResponse({"registration": "success", "email_sent": email_status}, status=200)
       
        except Exception as ex:
            return HttpResponse(f"error: {str(ex)}", status=500)
def _patient_update(request):
    patient_id = request.POST.get('id')
    try:
        patient = Patient.objects.get(pk=patient_id)
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth','phone_number', 'email', 'address']
        for field in fields:
            setattr(patient, field, request.POST.get(field))
        patient.save()
        return JsonResponse({"registration": "success",}, status=200)
       
    except Patient.DoesNotExist:
        return HttpResponse("Patient not found", status=404)
    except Exception as ex:
        return HttpResponse(f"error: {str(ex)}", status=500)
    
    
def home(request):
    # patients=Patient.objects.all()
    # return render(request,"patient/home.html",context={'patients':patients})    
    return redirect("user:login_view")
    
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    print(patients)
    return render(request,"patient/patient_list.html",context={'patients':patients})    
