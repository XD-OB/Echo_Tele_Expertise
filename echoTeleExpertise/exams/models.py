from django.db import models
from django.utils import timezone
from patients.models import Patient
from core.models import User
import datetime

# Model of the Request for opinion
class   Request(models.Model):
    is_urgent = models.BooleanField('La demande est urgente', default=False)
    exam_date = models.DateField("Date d'examen", default=timezone.now)
    subject = models.CharField('Objet', max_length=50)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    expert_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expert')
    text_doctor = models.TextField("Description du medecin", blank=True)
    text_expert = models.TextField("Description de l'expert", blank=True)
    is_incomplete = models.BooleanField('Des informations complémentaire sont necessaire', default=False)
    is_close = models.BooleanField('Le compte rendu est envoyé', default=False)
    is_doctor_visited = models.BooleanField("Cette demande est vue par l'auteur ", default=False)
    is_expert_visited = models.BooleanField("Cette demande est vue par l'expert", default=False)
    create_date = models.DateTimeField("Date de la demande", auto_now_add=True)
    solve_date = models.DateTimeField("Date d'envoi du rapprt", default=timezone.now)
    notification_date = models.DateTimeField("Date de la notification", default=timezone.now)

    def    __str__(self):
        return ('exam ' + str(self.pk))


# Model of the Documents and there relation with the Requests
class   Document(models.Model):
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/%Y-%M-%D', max_length=254)
    name = models.CharField('Name of the file', max_length=50)
    ext = models.CharField('extension du fichier', max_length=10)
    is_answer = models.BooleanField('Est un document joint à une réponse', default=False)

    def __str__(self):
        return self.name