from django.core.exceptions import ValidationError
from patients.models import Patient
from django import forms

class   RequestForm(forms.Form):
    exam_date = forms.DateField(label="Date d'examen")
    subject = forms.CharField(label='Objet', max_length=50)
    description = forms.CharField(label='Description', max_length=5000)

    # Clean the fields before puting them in the db:

    def     clean_subject(self):
        subject = self.cleaned_data['subject']
        # Remove extra whitespaces
        subject = ' '.join(subject.split())
        # Capitalize the subject
        subject = subject.capitalize()
        return subject
    
    def     clean_description(self):
        description = self.cleaned_data['description']
        # Remove extra whitespaces
        description = ' '.join(description.split())
        return description

#########################################################

class   PatientRequestForm(forms.Form):
    expert_id = forms.IntegerField(label="Expert id")
    exam_date = forms.DateField(label="Date d'examen")
    subject = forms.CharField(label='Objet', max_length=50)
    description = forms.CharField(label='Description', max_length=5000)

    # Clean the fields before puting them in the db:

    def     clean_subject(self):
        subject = self.cleaned_data['subject']
        # Remove extra whitespaces
        subject = ' '.join(subject.split())
        # Capitalize the subject
        subject = subject.capitalize()
        return subject
    
    def     clean_description(self):
        description = self.cleaned_data['description']
        # Remove extra whitespaces
        description = ' '.join(description.split())
        return description