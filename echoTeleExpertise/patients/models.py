from django.db import models
from core.models import User
from datetime import datetime
from echoTeleExpertise.consts import GENDER_CHOICES

# Patients Model
class   Patient(models.Model):
    last_name = models.CharField('Nom', max_length=20)
    first_name = models.CharField('Prénom', max_length=30)
    cin = models.CharField('CIN', max_length=15)
    gender = models.CharField('Sexe', max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField('Date de naissance')

    def     __str__(self):
        return (self.cin + ' | ' + self.last_name + ' ' + self.first_name)

# This Model is a relation many-to-many between Doctors & Patients
class   Relation(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField('Téléphone', max_length=10)
    join_date = models.DateTimeField('Date du premier contact', auto_now_add=True)

    def     __str__(self):
        return ('doctor ' + str(self.doctor_id) + ' | patient ' + str(self.patient_id))