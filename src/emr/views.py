import base64
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from emr.llm.llmai import _db_data_manipulate, _generate_image, _imaging_analysis, _speech_recognition, _text_generation
import user
from user.models import CustomUser
from .models import HPI, Doctor, Patient,MedicalRecord, PatientInTake, VitalSign
from datetime import date
from django.db.models import F, ExpressionWrapper, IntegerField, Case, When, Value
from django.db.models.functions import Now, ExtractYear, ExtractMonth, ExtractDay
from django.db.models.functions import TruncDate
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.contrib.auth.models import User
from datetime import datetime
# Create your views here.
def patient_list(request):
    return render(request, 'emr/patient_list.html') 
def medical_record_per_doctor(request):
        if not request.user.is_authenticated:
            return redirect('user:login_view')

        try:
            doctor_user = request.user
            print(doctor_user)
            doctor = Doctor.objects.get(doctor_user=doctor_user)
            print(doctor)
            medical_records=MedicalRecord.objects.filter(doctor=doctor)
            print(medical_records)
            return render(request,'emr/medicalrecord/medical_record_per_doctor.html',{'medical_records':medical_records,})
       
        except Doctor.DoesNotExist:
            return render(request, 'emr/medicalrecord/medical_record_per_doctor.html', {'error': 'Doctor not found.'})
            return render(request,'emr/medicalrecord/medical_record_per_doctor.html', {'patient_id': None})
        
        
        except Exception as e:
            return render(request,'emr/medicalrecord/medical_record_per_doctor.html', {'error': str(e)})


def medical_record_per_patient(request):
        patient_id = request.GET.get("patient_id")

        if not patient_id:
            return render(request,'emr/medicalrecord/medical_record.html', {'patient_id': None})
        
        try:
            patient_id = int(patient_id)
        except ValueError:
            return render(request,'emr/medicalrecord/medical_record.html', {'error': 'Invalid Patient ID.'})

        try:
            patient=Patient.objects.get(pk=patient_id)
            medical_records=MedicalRecord.objects.filter(patient=patient)
            doctors=Doctor.objects.all()
            return render(request,'emr/medicalrecord/medical_record.html',{'doctors':doctors,'patient':patient,'patient_id':patient_id,'medicalrecords':medical_records})
        except Patient.DoesNotExist:
            return render(request,'emr/medicalrecord/medical_record.html', {'error': 'Patient not found.'})
        except Exception as e:
            return render(request,'emr/medicalrecord/medical_record.html', {'error': str(e)})


def medical_charts_view(request):
    medical_record_id=request.GET.get("mr_id")
    medical_record=MedicalRecord.objects.get(id=medical_record_id)
    patient=Patient.objects.get(pk=medical_record.patient_id)
    vital_signs=VitalSign.objects.filter(medical_record=medical_record).order_by('-created_at')
    patient_intakes=PatientInTake.objects.filter(medical_record=medical_record).order_by('-created_at')
    hpis=HPI.objects.filter(medical_record=medical_record).order_by('-created_at')
    return render(request,'emr/medicalcharts/medical_charts.html',context={'patient':patient,
                                                                           'medical_record':medical_record,
                                                                            'vital_signs':vital_signs,
                                                                            'patient_intakes':patient_intakes,    
                                                                             'hpis':hpis})


def medical_record_save(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    if not request.POST.get('id'):
        return _medical_record_create(request)
    else:
        return _medical_record_update(request)
    
def  vital_sign_get(request,id:int):
      if request.method != "GET":
          return HttpResponse(status=405)
      try:
          vital_sign=VitalSign.objects.get(pk=id)
      except VitalSign.DoesNotExist:
          return HttpResponse("Vital Sign not found", status=404)
      except Exception:
          return HttpResponse(status=500)
      vs_json = serialize('json', [vital_sign,])
      return HttpResponse(vs_json, content_type='application/json',status=200)

def vital_sign_save(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    if not request.POST.get('id'):
        return _vital_sign_create(request)
    else:
        return _vital_sign_update(request)
def _vital_sign_update(request):
     vital_sign_id = request.POST.get('id')
     try:
        vital_sign = VitalSign.objects.get(pk=vital_sign_id)
        excluded_fields = ['id', 'created_at', 'updated_at','medical_record']
        fields = [field.name for field in VitalSign._meta.get_fields() if field.name not in excluded_fields]
        for field in fields:
            setattr(vital_sign, field, request.POST.get(field))
        vital_sign.save()
        return JsonResponse({"save_status": "success",}, status=200)
       
     except VitalSign.DoesNotExist:
        return HttpResponse("Vital Sign not found", status=404)
     except Exception as ex:
        return HttpResponse(f"error: {str(ex)}", status=500)
    
   

def _vital_sign_create(request):
        if request.method != "POST":
            return HttpResponse(status=405)

        try:
            print("in create")
            # Extract fields dynamically excluding specific ones
            excluded_fields = ['id', 'created_at', 'updated_at','medical_record', ]
            fields = [field.name for field in VitalSign._meta.get_fields() if field.name not in excluded_fields]
            # Collect patient data from POST request
            vital_sign_data = {
                field: (float(value) if VitalSign._meta.get_field(field).get_internal_type() == 'FloatField' else value)
                for field in fields if (value := request.POST.get(field)) is not None
            }
            vital_sign = VitalSign(**vital_sign_data)
            
            print(vital_sign)
            
            medical_record=MedicalRecord.objects.get(pk=int(request.POST.get('medical_record_id')))
            vital_sign.medical_record = medical_record
          
            vital_sign.save()

            return JsonResponse({"save_status": "success", "message": "Vital Sign created successfully."}, status=201)
        except Exception as ex:
            return JsonResponse({"save_status": "error", "message": str(ex)}, status=500)

  
def  hpi_get(request,id:int):
    if request.method != "GET":
        return HttpResponse(status=405)
    try:
        hpi = HPI.objects.get(pk=id)
    except HPI.DoesNotExist:
        return HttpResponse("HPI not found", status=404)
    except Exception:
        return HttpResponse(status=500)
    hpi_json = serialize('json', [hpi,])
    return HttpResponse(hpi_json, content_type='application/json', status=200)

def hpi_save(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    if not request.POST.get('id'):
        return _hpi_create(request)
    else:
        return _hpi_update(request)

def _hpi_update(request):
    hpi_id = request.POST.get('id')
    try:
        print("in update")
        
        hpi = HPI.objects.get(pk=hpi_id)
        excluded_fields = ['id', 'created_at', 'updated_at', 'medical_record']
        fields = [field.name for field in HPI._meta.get_fields() if field.name not in excluded_fields]
        for field in fields:
            setattr(hpi, field, request.POST.get(field))
        hpi.save()
        return JsonResponse({"save_status": "success"}, status=200)
    except HPI.DoesNotExist:
        return HttpResponse("HPI not found", status=404)
    except Exception as ex:
        return HttpResponse(f"error: {str(ex)}", status=500)

def _hpi_create(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        print("in create")
        # Extract fields dynamically excluding specific ones
        excluded_fields = ['id', 'created_at', 'updated_at', 'medical_record']
        fields = [field.name for field in HPI._meta.get_fields() if field.name not in excluded_fields]
        # Collect patient data from POST request
        hpi_data = {
            field: (float(value) if HPI._meta.get_field(field).get_internal_type() == 'FloatField' else value)
            for field in fields if (value := request.POST.get(field)) is not None
        }
        hpi = HPI(**hpi_data)

        print(hpi)

        medical_record = MedicalRecord.objects.get(pk=int(request.POST.get('medical_record_id')))
        hpi.medical_record = medical_record

        hpi.save()

        return JsonResponse({"save_status": "success", "message": "HPI created successfully."}, status=201)
    except Exception as ex:
        print(ex)
        return JsonResponse({"save_status": "error", "message": str(ex)}, status=500)



  
def  patient_intake_get(request,id:int):
    if request.method != "GET":
        return HttpResponse(status=405)
    try:
        patient_intake = PatientInTake.objects.get(pk=id)
    except PatientInTake.DoesNotExist:
        return HttpResponse("Patient Intake not found", status=404)
    except Exception:
        return HttpResponse(status=500)
    patient_intake_json = serialize('json', [patient_intake,])
    return HttpResponse(patient_intake_json, content_type='application/json', status=200)

def patient_intake_save(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    if not request.POST.get('id'):
        return _patient_intake_create(request)
    else:
        return _patient_intake_update(request)

def _patient_intake_update(request):
    patient_intake_id = request.POST.get('id')
    try:
        print("in update")
        
        patient_intake = PatientInTake.objects.get(pk=patient_intake_id)
        excluded_fields = ['id', 'created_at', 'updated_at', 'medical_record']
        fields = [field.name for field in PatientInTake._meta.get_fields() if field.name not in excluded_fields]
        for field in fields:
            setattr(patient_intake, field, request.POST.get(field))
        patient_intake.save()
        return JsonResponse({"save_status": "success"}, status=200)
    except PatientInTake.DoesNotExist:
        return HttpResponse("Patient Intake not found", status=404)
    except Exception as ex:
        return HttpResponse(f"error: {str(ex)}", status=500)

def _patient_intake_create(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        print("in create")
        
        
        print(request.POST.get("medical_record_id"))
        # Extract fields dynamically excluding specific ones
        excluded_fields = ['id', 'created_at', 'updated_at', 'medical_record']
        fields = [field.name for field in PatientInTake._meta.get_fields() if field.name not in excluded_fields]
        # Collect patient data from POST request
        patient_intake_data = {
            field: (float(value) if PatientInTake._meta.get_field(field).get_internal_type() == 'FloatField' else value)
            for field in fields if (value := request.POST.get(field)) is not None
        }
        patient_intake = PatientInTake(**patient_intake_data)
        
        print(patient_intake)

        medical_record = MedicalRecord.objects.get(pk=int(request.POST.get('medical_record_id')))
        patient_intake.medical_record = medical_record

        patient_intake.save()

        return JsonResponse({"save_status": "success", "message": "Patient Intake created successfully."}, status=201)
    except Exception as ex:
        print(ex)
        return JsonResponse({"save_status": "error", "message": str(ex)}, status=500)

def _medical_record_update(request):
    pass

def _medical_record_create(request):
        if request.method != "POST":
            return HttpResponse(status=405)

        try:
            # Extract fields dynamically excluding specific ones
            excluded_fields = ['id', 'created_at', 'updated_at','doctor', 'patient']
            patient= Patient.objects.get(pk=request.POST.get('patient_id'))
            doctor=Doctor.objects.get(pk=request.POST.get('doctor_id'))
            fields = [field.name for field in MedicalRecord._meta.get_fields() if field.name not in excluded_fields]
            
            # Collect patient data from POST request
            medical_record_data = {field: request.POST.get(field) for field in fields if field in request.POST}
        
            # Create and save the patient record
            medical_record = MedicalRecord(**medical_record_data)
            medical_record.patient = patient
            medical_record.doctor = doctor  
            medical_record.mr_code = f"MR{patient.id}-{date.today().strftime('%Y%m%d')}-{MedicalRecord.objects.filter(patient=patient).count() + 1}"
        
            print(medical_record)
            medical_record.save()

            return JsonResponse({"save_status": "success", "message": "Medical record created successfully."}, status=201)
        except Exception as ex:
            return JsonResponse({"save_status": "error", "message": str(ex)}, status=500)

def  patient_get(request,id:int):
    if request.method != "GET":
        return HttpResponse(status=405)
    try:
     patient=Patient.objects.get(pk=id)
    except:
        return HttpResponse(status=500)
    todo_json = serialize('json', [patient,])
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
            excluded_fields = ['id', 'created_at', 'updated_at']
            fields = [field.name for field in Patient._meta.get_fields() if field.name not in excluded_fields]
            # Collect patient data from POST request
            patient_data = {field: request.POST.get(field) for field in fields if field in request.POST}
            # Create and save the patient record
            patient = Patient(**patient_data)
          
            patient.save()
            email_sent = False or send_mail('Patient Registration Notification',
                      'Hi there,\n\You have been registered successfully in our app ,please use the patient portal from now on\n\nRegards,\n',
                        'Bereket Fiseha codigorey111@gmail.com',
                         ['bereketfiseha123@gmail.com'],
                         fail_silently=False,
                              )
            email_status = "success" if email_sent else "failed"
            return JsonResponse({"save_status": "success", "email_sent": email_status}, status=200)
       
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
    return render(request,"emr/registration/patient_list.html",context={'patients':patients})    
def doctor_list(request):
    doctors = Doctor.objects.all().order_by('-created_at')
    print(doctors)
    return render(request,"emr/registration/doctor_list.html",context={'doctors':doctors})    
def doctor_get(request,id:int):
    pass
def doctor_save(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    if not request.POST.get('id'):
        return _doctor_create(request)
    else:
        return _doctor_update(request)

def _doctor_create(request):
    if request.method == "POST":
        try:
            excluded_fields = ['id', 'created_at', 'updated_at']
            fields = [field.name for field in Doctor._meta.get_fields() if field.name not in excluded_fields]
            # Collect patient data from POST request
            doctor_data = {field: request.POST.get(field) for field in fields if field in request.POST}
            # Create and save the patient record
            
            # Generate unique username using firstname and current time (minute and second)
            current_time = datetime.now().strftime("%M%S")
            username = f"{doctor_data['first_name']}{current_time}"
            password = "pass1234"
          
            # Create a new user for the doctor
            doctor_user = CustomUser.objects.create_user(username=username, password=password)
            doctor_user.save()
            print(doctor_user)
            # Associate the user with the doctor
            doctor_data['doctor_user'] = doctor_user
            
            doctor = Doctor(**doctor_data)
            print(doctor)
            doctor.save()
            return JsonResponse({"save_status": "success"}, status=200)
       
        except Exception as ex:

            print(ex)
            return HttpResponse(f"error: {str(ex)}", status=500)
def _doctor_update(request):
    pass


def llm_chat(request):
    return render(request,"emr/llm/llmchat.html")    



#generic llm 




def get_ai_response(request):
    print("gen ai response")
    llm_task=request.POST.get("llm_task")
    model=request.POST.get("model")
    user_prompt=request.POST.get("user_prompt")
    chat_history=request.POST.get("chat_history")
    history = json.loads(chat_history) if chat_history else []
    # history.append({"role": "user", "content": user_prompt})
    audio = 'audio'
    llm_response=""
    print(llm_task)
    if llm_task=="db_manipulation":
         llm_response= _db_data_manipulate(model,user_prompt)
    
    elif llm_task=="medical_image_analysis":
        print("in medical image")
        if  not request.FILES.get('image'):
             return HttpResponse("No image was provided",status=400)
    
        else :
             image_file = request.FILES['image']
             user_prompt=""
             print(image_file)
             image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
             print(image_base64)
             llm_response= _imaging_analysis('jpg',image_base64,model,user_prompt)     
    elif llm_task=="speech recognition":
        llm_response=_speech_recognition(model,audio)     
    elif llm_task=="image generation":
          _generate_image()
    else:
        llm_response= _text_generation(model,user_prompt,history=history)   
        history.append({"role": "assistant", "content": llm_response})   

    return HttpResponse(llm_response)
