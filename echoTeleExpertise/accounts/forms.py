from django.core.exceptions import ValidationError
from core.models import User
from django import forms

class   RegisterForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Mot de passe', max_length=40)
    password2 = forms.CharField(label='Confirmation du mot de passe', max_length=40)
    first_name = forms.CharField(label='Prénom', max_length=30)
    last_name = forms.CharField(label='Nom', max_length=20)
    speciality = forms.CharField(label='Specialité', max_length=50)
    institution = forms.CharField(label='Etablissement', max_length=50)
    city = forms.CharField(label='Ville', max_length=20)
    address = forms.CharField(label='Adresse', max_length=80)
    phone = forms.CharField(label='Telephone', max_length=20)
    cin = forms.CharField(label='CIN', max_length=15)

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

    def     clean_speciality(self):
        speciality = self.cleaned_data['speciality']
        # Test if the speciality contain numbers
        if not speciality.isalpha():
            raise ValidationError("La specialité contient des nombres!")
        # Remove extra whitespaces
        speciality = ' '.join(speciality.split())
        # Capitalize the speciality
        speciality = speciality.capitalize()
        return speciality
    
    def     clean_institution(self):
        institution = self.cleaned_data['institution']
        # Remove extra whitespaces
        institution = ' '.join(institution.split())
        return institution
    
    def     clean_address(self):
        address = self.cleaned_data['address']
        # Remove extra whitespaces
        address = ' '.join(address.split())
        return address
    
    def     clean_city(self):
        city = self.cleaned_data['city']
        # Test if the citycontain numbers
        if not city.isalpha():
            raise ValidationError("La ville contient des nombres!")
        # Remove extra whitespaces
        city = ' '.join(city.split())
        # Capitalize the city
        city = city.capitalize()
        return city

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

    def     clean_email(self):
        email = self.cleaned_data['email']
        # Test if the email is used:
        if User.objects.filter(email=email, is_verified_mail=True).count() > 0:
            raise ValidationError("Cet email est déjà utilisé!")
        # Remove extra whitespaces
        email = ' '.join(email.split())
        # lowercase the email
        email = email.lower()
        return email

###############################################################

class   EditProfileForm(forms.Form):
    online_status = forms.BooleanField(label='La disponibilité')
    is_enable_mail = forms.BooleanField(label="Activer la reception d'email")
    first_name = forms.CharField(label='Prénom', max_length=30)
    last_name = forms.CharField(label='Nom', max_length=20)
    speciality = forms.CharField(label='Specialité', max_length=50)
    institution = forms.CharField(label='Etablissement', max_length=50)
    city = forms.CharField(label='Ville', max_length=20)
    address = forms.CharField(label='Adresse', max_length=80)
    phone = forms.CharField(label='Telephone', max_length=20)
    cin = forms.CharField(label='CIN', max_length=15)
    biography = forms.CharField(label='Biographie', max_length=1500)

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

    def     clean_speciality(self):
        speciality = self.cleaned_data['speciality']
        # Test if the speciality contain numbers
        if not speciality.isalpha():
            raise ValidationError("La specialité contient des nombres!")
        # Remove extra whitespaces
        speciality = ' '.join(speciality.split())
        # Capitalize the speciality
        speciality = speciality.capitalize()
        return speciality
    
    def     clean_institution(self):
        institution = self.cleaned_data['institution']
        # Remove extra whitespaces
        institution = ' '.join(institution.split())
        return institution
    
    def     clean_address(self):
        address = self.cleaned_data['address']
        # Remove extra whitespaces
        address = ' '.join(address.split())
        return address
    
    def     clean_city(self):
        city = self.cleaned_data['city']
        # Test if the citycontain numbers
        if not city.isalpha():
            raise ValidationError("La ville contient des nombres!")
        # Remove extra whitespaces
        city = ' '.join(city.split())
        # Capitalize the city
        city = city.capitalize()
        return city

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

    def     clean_biography(self):
        biography = self.cleaned_data['biography']
        # Capitalize
        biography = biography.capitalize()
        # Remove extra whitespaces
        biography = ' '.join(biography.split())
        return biography
