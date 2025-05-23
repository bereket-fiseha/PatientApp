from . import views
from django.urls import path
app_name="patientapp"

urlpatterns = [
     path('patient/',views.patient_list, name='patient_list_view'),
     path('patient/create',views.patient_create, name='patient_create'),
     path('patient/update',views.patient_update, name='patient_update'),
     
     path('',views.home, name='home_view'),
    
]
