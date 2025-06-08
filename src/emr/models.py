import math
from django.db import models
from datetime import date

from user.models import CustomUser

# Create your models here.

class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    specialization = models.CharField(max_length=50)
    email = models.EmailField()
    doctor_user = models.ForeignKey(
    CustomUser,  # Replace with the actual custom user model class
    on_delete=models.CASCADE,
    blank=True,  # Allow this field to be optional
    null=True,   # Allow this field to be nullable
)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name



class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    #mrn=models.CharField(max_length=20, unique=True)
     
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender=models.CharField(max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    address = models.TextField()
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class MedicalRecord(models.Model):
      doctor=models.ForeignKey(Doctor,related_name="assigned_medical_records",on_delete=models.DO_NOTHING)
      patient=models.ForeignKey(Patient,related_name="medical_records",on_delete=models.CASCADE)
      chief_complaint=models.TextField()
      symptome_details=models.TextField()

      pain_scale=models.TextField()
         
      created_at = models.DateTimeField(auto_now_add=True)
      mr_code=models.CharField(max_length=20, unique=True)
      service_date=models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True) 
      def __str__(self):
        return f"{self.patient.first_name} {self.chief_complaint}"


      

class VitalSign(models.Model):
      medical_record=models.ForeignKey(MedicalRecord,related_name="vital_signs",on_delete=models.CASCADE)
      pulse_rate=models.FloatField()
      respiratory_rate=models.FloatField()
      temprature=models.FloatField()
      height=models.FloatField()
      weight=models.FloatField()
      blood_pressure=models.CharField(max_length=20)  # e.g., "120/80 mmHg"
      blood_oxygen_saturation=models.CharField(max_length=10)  # e.g., "98%"
      balance=models.CharField(max_length=20)  # e.g., "Normal", "Abnormal"
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True) 
      @property
      def BMI(self):
        return self.weight/math.pow(self.height,2)      
      def __str__(self):
          return f"vital sign with {self.BMI}" 

class HPI(models.Model):
      medical_record=models.ForeignKey(MedicalRecord,related_name="hpis",on_delete=models.CASCADE)
      hpi_note=models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True) 
      def __str__(self):
        return self.hpi_note

class ReviewOfSystem(models.Model):
    medical_record=models.ForeignKey(MedicalRecord,related_name="review_of_systems",on_delete=models.CASCADE)
    general = models.TextField(blank=True, null=True)
    skin = models.TextField(blank=True, null=True)
    heent = models.TextField(blank=True, null=True)  # Head, eyes, ears, nose, throat
    neck = models.TextField(blank=True, null=True)
    breasts = models.TextField(blank=True, null=True)
    respiratory = models.TextField(blank=True, null=True)
    cardiovascular = models.TextField(blank=True, null=True)
    gastrointestinal = models.TextField(blank=True, null=True)
    genitourinary = models.TextField(blank=True, null=True)
    endocrine = models.TextField(blank=True, null=True)
    neurological = models.TextField(blank=True, null=True)
    psychiatric = models.TextField(blank=True, null=True)
    musculoskeletal = models.TextField(blank=True, null=True)
    hematologic_lymphatic = models.TextField(blank=True, null=True)
    allergic_immunologic = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      return f"Review of Systems for {self.medical_record.patient}"
      

class Assessment(models.Model):
      medical_record=models.ForeignKey(MedicalRecord,related_name="assessments",on_delete=models.CASCADE)
      assessment_note=models.TextField()

      diferential_diagnosis=models.TextField(blank=True, null=True)  # AI-generated differential diagnosis

      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True) 
      def __str__(self):
        return self.Note
class Plan(models.Model):
    medical_record=models.ForeignKey(MedicalRecord,related_name="plan",on_delete=models.CASCADE)
    plan_note=models.TextField()
    ai_plan=models.TextField(blank=True, null=True)  # AI-generated plan
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
      return self.note
    
class PatientInTake(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, related_name="intake_forms", on_delete=models.CASCADE)
    chief_complaint = models.TextField()
    past_medical_history = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    allergies = models.TextField()
    family_history = models.TextField(blank=True)
    social_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Intake form for  - {self.chief_complaint}"
class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, related_name="prescriptions", on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.medical_record.patient.full_name} - {self.medication_name}"     
