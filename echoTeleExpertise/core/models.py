from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from echoTeleExpertise.consts import DISPONIBILITY_CHOICES
from .managers import UserManager

class   User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Prénom', max_length=30)
    last_name = models.CharField('Nom', max_length=20)
    speciality = models.CharField('Specialité', max_length=50)
    institution = models.CharField('Etablissement', max_length=50)
    city = models.CharField('Ville', max_length=20)
    address = models.CharField('Adresse', max_length=80)
    phone = models.CharField('Telephone', max_length=20)
    cin = models.CharField('CIN', max_length=15)
    date_joined = models.DateTimeField('Date du rejoint', auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', default='avatars/empty_profile.jpg')
    biography = models.TextField('Biographie', blank=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Personnel', default=False)
    count_opinion = models.IntegerField('Nombre des aides délivrer', default=0)
    online_status = models.CharField('Status onligne', max_length=9, choices=DISPONIBILITY_CHOICES, default='AVAILABLE')
    is_enable_mail = models.BooleanField('Envoyer les nouvautés en email', default=True)
    is_verified_mail = models.BooleanField("L'email est verifié", default=False)
    
    def __str__(self):
        return self.email

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class   Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'