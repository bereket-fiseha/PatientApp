from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('admin', 'Admin'),
        
        ('triage', 'Triage')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
