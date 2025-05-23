from . import views
from django.urls import path
app_name="user"

urlpatterns = [
   
    path('register/',views.register_view, name='register_view'),
    
    path('login/',views.login_view, name='login_view'),
]
