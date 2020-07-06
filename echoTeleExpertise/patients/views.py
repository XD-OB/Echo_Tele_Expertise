from django.http import Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from mylib.notifications import get_summary_notifs
from .forms import PatientForm, EditPatientForm
from .models import Patient, Relation
from django.contrib import messages
from datetime import datetime

# Patient Detail
@login_required
def     patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    phone = Relation.objects.values_list('phone', flat=True).get(
        patient_id=patient_id,
        doctor_id=request.user
    )
    other_phones = Relation.objects.filter(
        patient_id=patient_id
    ).exclude(
        doctor_id=request.user
    ).order_by('-join_date').values_list('phone', flat=True)
    context = {
        'patient': patient,
        'main_phone': phone,
        'phones': other_phones,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'patients/patient.html', context)


# Edit Patient
@login_required
def     edit_patient(request, patient_id):
    # Get the patient with th id = patient_id from the database
    patient = get_object_or_404(Patient, pk=patient_id)
    # Get the relation doctor/patient from the database
    try:
        relation = Relation.objects.get(
            patient_id=patient_id,
            doctor_id=request.user
        )
    except Relation.DoesNotExist:
        raise Http404("No Relation with this query.")
    # if the request is made with the method POST (the user submit some informations)
    if request.method == 'POST':
        form = EditPatientForm(request.POST)
        values = request.POST
        if form.is_valid():
            # Get infos
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            phone = form.cleaned_data['phone']
            birthdate = request.POST['birthdate']
            gender = request.POST['gender']
            # Edit Infos
            patient.last_name = last_name
            patient.first_name = first_name
            patient.gender = gender
            patient.birthdate = birthdate
            relation.phone = phone
            # Save modifications in the database
            relation.save()
            patient.save()
            messages.success(request, 'La modification est enregister')
    else:
        form = EditPatientForm()
        values = {}
    context = {
        'form': form,
        'values': values,
        'patient': patient,
        'phone': relation.phone,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'patients/edit_patient.html', context)


# Delete Patient
@login_required
def     delete_patient(request, patient_id):
    if request.method == 'POST':
        Relation.objects.filter(
            doctor_id=request.user,
            patient_id=patient_id
        ).delete()
        # If the patient doesn't have other relations with other doctors, we delete his account
        if not Relation.objects.filter(patient_id=patient_id).exists():
            Patient.objects.filter(pk=patient_id).delete()
        messages.success(request, 'Le patient est supprimer avec succès')
        return redirect('pages:list_patients')
    return HttpResponseNotAllowed('Not allowed to go to this page')


# Add New Patient
@login_required
def     add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        values = request.POST
        if form.is_valid():
            # Get patient infos:
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            cin = form.cleaned_data['cin']
            phone = form.cleaned_data['phone']
            gender = request.POST.get('gender', 'Homme')
            birthdate = request.POST.get('birthdate', datetime.now())
            # Check if the CIN is already used with this doctor:
            if Patient.objects.filter(
                pk__in=Relation.objects.filter(doctor_id=request.user).values_list('patient_id', flat=True),
                cin=cin
                ).exists():
                patient = Patient.objects.get(cin=cin)
                # Check if data entred by the user is like the one in the db
                if patient.first_name != first_name or patient.last_name != last_name or patient.gender != gender or patient.birthdate != birthdate:
                    messages.error(request, 'Faux informations! Un autre patient est déjà enregistrer avec ce C.I.N ou ce patient a donné une fause information!')
                    return redirect('patients:add_patient')
            else:
                patient = Patient(
                    last_name=last_name,
                    first_name=first_name,
                    cin=cin,
                    birthdate=birthdate,
                    gender=gender
                )
                # Save the new patient in the db
                patient.save()
            # Create the relation between the logged doctor and the new patient
            if Relation.objects.filter(doctor_id=request.user, patient_id=patient).exists():
                messages.warning(request, 'Vous avez déjà ce patient dans votre base de données!')
            else:
                relation = Relation(
                    doctor_id=request.user,
                    patient_id=patient,
                    phone=phone
                )
                # Save the relation
                relation.save()
                messages.success(request, 'Le nouveau patient est ajouté avec succès')
            return redirect('patients:add_patient')
    else:
        form = PatientForm()
        values = {}
    context = {
        'form': form,
        'values': values,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'patients/add_patient.html', context)