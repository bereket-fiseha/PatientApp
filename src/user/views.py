from importlib import reload
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
# Create your views here.

from django.core.mail import send_mail
def register_view(request):
    if request.method=="POST":
       form=UserCreationForm(request.POST)
 
       if form.is_valid():
         form.save()
         return redirect("user:login_view") 
       else:
           print(form.errors)
    form=UserCreationForm()
    return render(request,"user/register.html",{'form':form})

def logout_view(request):
      if request.method=="GET":
            logout(request=request)
     
            return redirect("user:login_view")
      

def login_view(request):
     if request.method=="POST":
          print("in")
          form=AuthenticationForm(data=request.POST)

          if form.is_valid():

                login(request,form.get_user())
                return redirect("patientapp:patient_list_view")
          else:
               return HttpResponse("Invalid credentials")
      
     form=AuthenticationForm()
     
     return render(request,"user/login.html",{'form':form})
