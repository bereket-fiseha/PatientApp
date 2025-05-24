from . import views
from django.urls import path
app_name="patientapp"

urlpatterns = [
     path('patient/',views.patient_list, name='patient_list_view'),
     path('patient/save',views.patient_save, name='patient_save'),
    # path('patient/update',views.patient_update, name='patient_update'),
        path('patient/<int:id>',views.patient_get, name='patient_get'),
     
     path('',views.home, name='home_view'),
    
]
