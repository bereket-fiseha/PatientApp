from . import views
from django.urls import path
app_name="emrapp"

urlpatterns = [
     path('patient/',views.patient_list, name='patient_view'),
     path('patient/save',views.patient_save, name='patient_save'),
    # path('patient/update',views.patient_update, name='patient_update'),
        path('patient/<int:id>',views.patient_get, name='patient_get'),
     path('medicalrecord/',views.medical_record_per_patient, name='medical_record_per_patient'),
    path('mymedicalrecord/',views.medical_record_per_doctor, name='medical_record_per_doctor'),
    
    
       path('medicalrecord/save',views.medical_record_save, name='medical_record_save'),
  
path('doctor/',views.doctor_list, name='doctor_view'),
     path('doctor/save',views.doctor_save, name='doctor_save'),
    # path('patient/update',views.patient_update, name='patient_update'),
        path('doctor/<int:id>',views.doctor_get, name='doctor_get'),
  
     
  path('medicalrecord/medicalcharts',views.medical_charts_view, name='medical_charts_view'),
     path('medicalrecord/vitalsign/save',views.vital_sign_save, name='vital_sign_save'),
    path('medicalrecord/vitalsign/<int:id>',views.vital_sign_get, name='vital_sign_get'),
    
     path('medicalrecord/hpi/save',views.hpi_save, name='hpi_save'),
    path('medicalrecord/hpi/<int:id>',views.hpi_get, name='hpi_get'),


     path('medicalrecord/patientintake/save',views.patient_intake_save, name='patient_intake_save'),
    path('medicalrecord/patientintake/<int:id>',views.patient_intake_get, name='patient_intake_get'),


path('ai/get_response',views.get_ai_response ,name="get_ai_response"),
    
     path('',views.home, name='home_view'),
    









path('ai/chat',views.llm_chat ,name="llm_chat"),
    


]
