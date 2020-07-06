from django.core.exceptions import ValidationError
from django import forms

class   PatientForm(forms.Form):
    gender = forms.CharField(label='Sexe', max_length=1)
    first_name = forms.CharField(label='Prénom', max_length=30)
    last_name = forms.CharField(label='Nom', max_length=20)
    phone = forms.CharField(label='Telephone', max_length=20)
    cin = forms.CharField(label='CIN', max_length=15)
    birthdate = forms.DateField(label='Date de naissance')

    # Clean the fields before puting them in the db:

    def     clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        # Test if the first_name contain numbers
        if not first_name.isalpha():
            raise ValidationError("Le prénom contient des nombres!")
        # Remove extra whitespaces
        first_name = ' '.join(first_name.split())
        # Capitalize the firstname
        first_name = first_name.capitalize()
        return first_name
    
    def     clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        # Test if the last_name contain numbers
        if not last_name.isalpha():
            raise ValidationError("Le nom contient des nombres!")
        # Remove extra whitespaces
        last_name = ' '.join(last_name.split())
        # Capitalize the lastname
        last_name = last_name.capitalize()
        return last_name

    def     clean_phone(self):
        phone = self.cleaned_data['phone']
        # Test if the first_name contain numbers
        chars = set('0123456789+-()')
        for c in phone:
            if not c in chars:
                raise ValidationError("Le numéro du téléphone doit contenir just '0123456789+-()' !")
        # Remove extra whitespaces
        phone = ' '.join(phone.split())
        return phone

    def     clean_cin(self):
        cin = self.cleaned_data['cin']
        # Test if the cin contain alphabetics and numbers
        if not cin.isalnum():
            raise ValidationError("Le C.I.N ne doit pas contenir des caractères spéciaux!")
        # Remove extra whitespaces
        cin = ' '.join(cin.split())
        # Uppercase the CIN
        cin = cin.upper()
        return cin

#############################################################

class   EditPatientForm(forms.Form):
    gender = forms.CharField(label='Sexe', max_length=1)
    first_name = forms.CharField(label='Prénom', max_length=30)
    last_name = forms.CharField(label='Nom', max_length=20)
    phone = forms.CharField(label='Telephone', max_length=20)
    birthdate = forms.DateField(label='Date de naissance')

    # Clean the fields before puting them in the db:

    def     clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        # Test if the first_name contain numbers
        if not first_name.isalpha():
            raise ValidationError("Le prénom contient des nombres!")
        # Remove extra whitespaces
        first_name = ' '.join(first_name.split())
        # Capitalize the firstname
        first_name = first_name.capitalize()
        return first_name
    
    def     clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        # Test if the last_name contain numbers
        if not last_name.isalpha():
            raise ValidationError("Le nom contient des nombres!")
        # Remove extra whitespaces
        last_name = ' '.join(last_name.split())
        # Capitalize the lastname
        last_name = last_name.capitalize()
        return last_name

    def     clean_phone(self):
        phone = self.cleaned_data['phone']
        # Test if the first_name contain numbers
        chars = set('0123456789+-()')
        for c in phone:
            if not c in chars:
                raise ValidationError("Le numéro du téléphone doit contenir just '0123456789+-()' !")
        # Remove extra whitespaces
        phone = ' '.join(phone.split())
        return phone