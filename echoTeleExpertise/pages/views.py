from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from echoTeleExpertise.consts import paginator_max, ete_email
from mylib.names import str_docname, str_fullname
from mylib.notifications import get_summary_notifs
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from exams.models import Request, Document
from patients.models import Patient, Relation
from core.models import User
from datetime import datetime
from os.path import basename
from functools import reduce
import operator
# The search is insensible for cases


@login_required
def     list_patients(request):
    '''
    View used to list the patients
    The Patients are ordered Ascendent Alphabeticaly with there last name
    '''
    my_relations = Relation.objects.filter(doctor_id__pk=request.user.pk).order_by('patient_id__last_name')
    # Filters using search bar inputs:
    ## Name
    if 'search_name' in request.GET:
        search_name = request.GET['search_name']
        if search_name:
            my_relations = my_relations.filter(
                Q(patient_id__last_name__startswith=search_name) |
                Q(patient_id__first_name__startswith=search_name)
            )
    ## C.I.N
    if 'search_cin' in request.GET:
        search_cin = request.GET['search_cin']
        if search_cin:
            my_relations = my_relations.filter(patient_id__cin__icontains=search_cin)
    ## Gender
    if 'search_gender' in request.GET:
        search_gender = request.GET['search_gender']
        if search_gender:
            my_relations = my_relations.filter(patient_id__gender__iexact=search_gender)
    # Show val(paginator_max) elements
    paginator = Paginator(my_relations, paginator_max)
    page_number = request.GET.get('page')
    paged_relations = paginator.get_page(page_number)
    context = {
        'relations': paged_relations,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user),
        # Resend the previous inputs of the user
        'values': request.GET
    }
    return render(request, 'pages/list_patients.html', context)


@login_required
def     telefiles(request):
    '''
    View used to list the telefiles
    The Telefiles are ordered descendant by date of creation
    '''
    requests = Request.objects.filter(
        expert_id=request.user,
        is_incomplete=False,
        is_close=False
        ).order_by('-create_date')
    # From all the requests take the choices:
    original_requests = requests
    # Filter using search bar inputs:
    ## Is Urgent
    if 'search_urgent' in request.GET:
        search_urgent = request.GET['search_urgent']
        if search_urgent:
            requests = requests.filter(is_urgent=True)
    ## Patient:
    if 'search_patient' in request.GET:
        search_patient = request.GET['search_patient']
        if search_patient:
            requests = requests.filter(patient_id=search_patient)
    ## Owner of the request:
    if 'search_doctor' in request.GET:
        search_doctor = request.GET['search_doctor']
        if search_doctor:
            requests = requests.filter(doctor_id=search_doctor)
    ## Subject:
    if 'search_subject' in request.GET:
        search_subject = request.GET['search_subject']
        if search_subject:
            requests = requests.filter(subject__icontains=search_subject)
    # Show val(paginator_max) elements
    paginator = Paginator(requests, paginator_max)
    page_number = request.GET.get('page')
    paged_requests = paginator.get_page(page_number)
    context = {
        'requests': paged_requests,
        # Set of unique values of patients that have requests for the select search
        'unique_patients': Patient.objects.filter(
            pk__in=set(original_requests.values_list('patient_id', flat=True))
            ).order_by('last_name'),
        # Set of unique values of doctors that send requests for the select search
        'unique_doctors': User.objects.filter(
            pk__in=set(original_requests.values_list('doctor_id', flat=True))
            ).order_by('last_name'),
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user),
        # Resend the previous inputs of the user
        'values': request.GET
    }
    return render(request, 'pages/telefiles.html', context)


# Share the telefile:
def     share_telefile(request, request_id):
    req = get_object_or_404(Request, pk=request_id)
    experts = User.objects.filter(
        is_staff=False,
        is_active=True
    ).exclude(
        pk=request.user.pk
    ).exclude(
        pk=req.doctor_id.pk
    )
    # The Select Expert Filter
    if 'search_speciality' in request.GET:
        search_speciality = request.GET['search_speciality']
        if search_speciality:
            experts = experts.filter(speciality=search_speciality)
    if 'search_city' in request.GET:
        search_city = request.GET['search_city']
        if search_city:
            experts = experts.filter(city=search_city)
    documents = Document.objects.filter(request_id=request_id)
    context = {
        'req': req,
        'experts': experts,
        'documents': documents,
        'values': request.GET,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'pages/share_telefile.html', context)


# Share the request with other doctors:
## This fonction for combining the description of the owner and the doctor how seek other help
def     combine_descriptions(req, text_additional):
    if text_additional:
        old_owner = 'Dr ' + req.doctor_id.last_name + ' ' + req.doctor_id.first_name + ':\n'
        new_owner = 'Dr ' + req.expert_id.last_name + ' ' + req.expert_id.first_name + ':\n'
        return old_owner + req.text_doctor + '\n\n' + new_owner + text_additional
    return req.text_doctor

@login_required
def     share_request(request, request_id):
    '''
    View used to send the rapport for a request
    '''
    if request.method == 'POST':
        expert_id = request.POST['expert']
        new_subject = request.POST['new_subject']
        text_additional = request.POST['text_additional']
        is_urgent = request.POST.get('is_urgent', 'NONE')
        if expert_id:
            expert = get_object_or_404(User, pk=expert_id)
            req = get_object_or_404(Request, pk=request_id)
            # Duplicate the old request with new owner and expert:
            new_req = Request.objects.create(
                exam_date=req.exam_date,
                text_doctor=combine_descriptions(req, text_additional),
                subject= new_subject,
                patient_id=req.patient_id,
                doctor_id=request.user,
                expert_id=expert,
            )
            # The new owner of the request is the one how decide if the new request is urgent!
            if is_urgent == 'URGENT':
                new_req.is_urgent = True
            new_req.save()
            # Duplicate the files for the new request
            documents = Document.objects.filter(request_id=request_id)
            for document in documents:
                new_doc = Document.objects.create(
                    request_id=new_req,
                    file=document.file,
                    name=basename(document.name),
                    ext=document.name.rsplit('.', 1)[1],
                )
                new_doc.save()
            # The new files added by the new owner of the request:
            new_files = request.FILES.getlist('new_files')
            if new_files:
                for f in new_files:
                    document = Document.objects.create(
                        request_id=new_req,
                        file=f,
                        name=basename(f.name),
                        ext=f.name.rsplit('.', 1)[1]
                    )
                    document.save()
            # Send the Share Request Email to the Owner
            if req.expert_id.is_enable_mail:
                send_mail(
                    # Subject
                    "ETE: Un médecin a partager avec vous son télé-dossier pour avoir votre avis d'expertise.",
                    # Message
                    "La demande:\nL'objet: " + req.subject  + ".\nDemandeur d'avis: " + str_docname(req.doctor_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                    # From (Email)
                    ## A variable that contain the ete mail
                    ete_email,
                    # To (Email)
                    [req.expert_id.email, ],
                    # If the send fail do not affich any errors
                    fail_silently = True
                )
            messages.success(request, "Votre demande d'une autre avis d'expertise est envoyé.")
            # Add the contribution of the user to the counter in the db
            return redirect('pages:telefiles')
        messages.error(request, 'Vous deverez selectionner un médecin pour partager la demande!')
        return HttpResponseRedirect('/pages/telefile/' + str(request_id))


@login_required
def     send_rapport(request, request_id):
    '''
    View used to send the rapport for a request
    '''
    if request.method == 'POST':
        # Add the new infos then save
        req = get_object_or_404(Request, pk=request_id)
        req.text_expert = request.POST['text_expert']
        # Mark it unseen for the owner:
        req.is_doctor_visited = False
        req.solve_date = datetime.now()
        req.notifications_date = datetime.now()
        req.is_close = True
        req.save()
        # Add and Save the document in db
        files = request.FILES.getlist('files')
        for f in files:
            document = Document.objects.create(
                request_id=req,
                file=f,
                name=basename(f.name),
                ext=f.name.rsplit('.', 1)[1],
                is_answer=True
            )
            document.save()
        # Send the Done Request Email to the Owner
        if req.doctor_id.is_enable_mail:
            send_mail(
                # Subject
                "ETE: L'expert a envoyé son avis d'expertise pour votre demande.",
                # Message
                "La demande compléter:\nL'objet: " + req.subject  + ".\nL'expert: " + str_docname(req.expert_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                # From (Email)
                ## A variable that contain the ete mail
                ete_email,
                # To (Email)
                [req.doctor_id.email, ],
                # If the send fail do not affich any errors
                fail_silently = True
            )
        messages.success(request, "Votre avis d'expertise est envoyé!")
        # Add the contribution of the user to the counter in the db
        request.user.count_opinion += 1
        request.user.save()
        return redirect('pages:telefiles')
    return HttpResponseNotAllowed('Not allowed to go to this page')


@login_required
def     telefile(request, request_id):
    '''
    View used to show the detail of a specifique
    telefile with the id = request_id 
    '''
    req = get_object_or_404(Request, pk=request_id)
    # Mark the telefile as visited
    req.is_expert_visited = True
    req.notification_date = datetime.now()
    req.save()
    documents = Document.objects.filter(request_id=request_id)
    context = {
        'req': req,
        'documents': documents,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'pages/telefile.html', context)


@login_required
def     list_requests(request):
    '''
    View used to list the requests for experts opinions
    The Requests are ordered descendant by date of creation
    '''
    requests = Request.objects.filter(
        doctor_id=request.user,
        is_close=False
        ).order_by('-create_date')
    # From all the requests take the search choices:
    original_requests = requests
    # Filter using search bar inputs:
    ## Is Urgent
    if 'search_urgent' in request.GET:
        search_urgent = request.GET['search_urgent']
        if search_urgent:
            requests = requests.filter(is_urgent=True)
    ## Is Incomplete
    if 'search_incomplete' in request.GET:
        search_incomplete = request.GET['search_incomplete']
        if search_incomplete:
            requests = requests.filter(is_incomplete=True)
    ## Patient:
    if 'search_patient' in request.GET:
        search_patient = request.GET['search_patient']
        if search_patient:
            requests = requests.filter(patient_id=search_patient)
    ## Expert:
    if 'search_expert' in request.GET:
        search_expert = request.GET['search_expert']
        if search_expert:
            requests = requests.filter(expert_id=search_expert)
    ## Subject:
    if 'search_subject' in request.GET:
        search_subject = request.GET['search_subject']
        if search_subject:
            requests = requests.filter(subject__icontains=search_subject)
    # Show val(paginator_max) elements
    paginator = Paginator(requests, paginator_max)
    page_number = request.GET.get('page')
    paged_requests = paginator.get_page(page_number)
    context = {
        'requests': paged_requests,
        # Set of unique values of patients that have requests for the select search
        'unique_patients': Patient.objects.filter(
            pk__in=set(original_requests.values_list('patient_id', flat=True))
            ).order_by('last_name'),
        # Set of unique values of Expert that have requests for the select search
        'unique_experts': User.objects.filter(
            pk__in=set(original_requests.values_list('expert_id', flat=True))
            ).order_by('last_name'),
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user),
        # Resend the previous inputs of the user
        'values': request.GET
    }
    return render(request, 'pages/list_requests.html', context)


@login_required
def     list_doctors(request):
    '''
    View used to list the doctors
    The doctors are ordered Ascendent Alphabeticaly with there last name
    '''
    users = User.objects.filter(
        is_staff=False,
        is_active=True
        ).exclude(
            email=request.user.email
            ).order_by('last_name')
    # Filter using search bar inputs:
        ## Available
    if 'search_available' in request.GET:
        search_available = request.GET['search_available']
        if search_available:
            users = users.filter(online_status='AVAILABLE')
    ## Name
    if 'search_name' in request.GET:
        search_name = request.GET['search_name']
        if search_name:
            users = users.filter(
                Q(last_name__istartswith=search_name) |
                Q(first_name__istartswith=search_name)
            )
    ## Speciality
    if 'search_speciality' in request.GET:
        search_speciality = request.GET['search_speciality']
        if search_speciality:
            users = users.filter(speciality__startswith=search_speciality)
    ## Institution
    if 'search_institution' in request.GET:
        search_institution = request.GET['search_institution']
        if search_institution:
            users = users.filter(institution__icontains=search_institution)
    ## City
    if 'search_city' in request.GET:
        search_city = request.GET['search_city']
        if search_city:
            users = users.filter(city__startswith=search_city)
    # Show val(paginator_max) elements
    paginator = Paginator(users, paginator_max)
    page_number = request.GET.get('page')
    paged_users = paginator.get_page(page_number)
    context = {
        'doctors': paged_users,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user),
        # Resend the previous inputs of the user
        'values': request.GET
    }
    return render(request, 'pages/list_doctors.html', context)


@login_required
def     doctor(request, doctor_id):
    '''
    View used to show the detail of a specifique
    doctor with the id = doctor_id 
    '''
    doctor = get_object_or_404(User, pk=doctor_id)
    context = {
        'doctor': doctor,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'pages/doctor.html', context)


@login_required
def     requests_history(request):
    '''
    View used to list the completed requests of the user
    The Requests are ordered descendant by date of creation
    '''
    requests = Request.objects.filter(
        doctor_id=request.user,
        is_close=True
        ).order_by('-create_date')
    # From all the requests take the search choices:
    original_requests = requests
    # Filter using search bar inputs:
    ## Is Urgent
    if 'search_urgent' in request.GET:
        search_urgent = request.GET['search_urgent']
        if search_urgent:
            requests = requests.filter(is_urgent=True)
    ## Patient:
    if 'search_patient' in request.GET:
        search_patient = request.GET['search_patient']
        if search_patient:
            requests = requests.filter(patient_id=search_patient)
    ## Expert:
    if 'search_expert' in request.GET:
        search_expert = request.GET['search_expert']
        if search_expert:
            requests = requests.filter(expert_id=search_expert)
    ## Exam Date:
    if 'search_exam_date' in request.GET:
        search_exam_date = request.GET['search_exam_date']
        if search_exam_date:
            requests = requests.filter(exam_date=search_exam_date)
    ## Subject:
    if 'search_subject' in request.GET:
        search_subject = request.GET['search_subject']
        if search_subject:
            requests = requests.filter(subject__icontains=search_subject)
    # Show val(paginator_max) elements
    paginator = Paginator(requests, paginator_max)
    page_number = request.GET.get('page')
    paged_requests = paginator.get_page(page_number)
    context = {
        'requests': paged_requests,
        # Set of unique values of patients that have requests for the select search
        'unique_patients': Patient.objects.filter(
            pk__in=set(original_requests.values_list('patient_id', flat=True))
            ).order_by('last_name'),
        # Set of unique values of Expert that have requests for the select search
        'unique_experts': User.objects.filter(
            pk__in=set(original_requests.values_list('expert_id', flat=True))
            ).order_by('last_name'),
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user),
        # Resend the previous inputs of the user
        'values': request.GET
    }
    return render(request, 'pages/requests_history.html', context)


def     opinions_history(request):
    '''
    View used to list the completed telefiles of the user
    The Opinions are ordered descendant by date of solve
    '''
    requests = Request.objects.filter(
        expert_id=request.user,
        is_close=True
        ).order_by('-solve_date')
    # From all the requests take the search choices:
    original_requests = requests
    # Filter using search bar inputs:
    ## Is Urgent
    if 'search_urgent' in request.GET:
        search_urgent = request.GET['search_urgent']
        if search_urgent:
            requests = requests.filter(is_urgent=True)
    ## Patient:
    if 'search_patient' in request.GET:
        search_patient = request.GET['search_patient']
        if search_patient:
            requests = requests.filter(patient_id=search_patient)
    ## Request owner:
    if 'search_doctor' in request.GET:
        search_doctor = request.GET['search_doctor']
        if search_doctor:
            requests = requests.filter(doctor_id=search_doctor)
    ## Exam Date:
    if 'search_exam_date' in request.GET:
        search_exam_date = request.GET['search_exam_date']
        if search_exam_date:
            requests = requests.filter(exam_date=search_exam_date)
    ## Subject:
    if 'search_subject' in request.GET:
        search_subject = request.GET['search_subject']
        if search_subject:
            requests = requests.filter(subject__icontains=search_subject)
    # Show val(paginator_max) elements
    paginator = Paginator(requests, paginator_max)
    page_number = request.GET.get('page')
    paged_requests = paginator.get_page(page_number)
    context = {
        'requests': paged_requests,
        # Set of unique values of patients that have requests for the select search
        'unique_patients': Patient.objects.filter(
            pk__in=set(original_requests.values_list('patient_id', flat=True))
            ).order_by('last_name'),
        # Set of unique values of Expert that have requests for the select search
        'unique_doctors': User.objects.filter(
            pk__in=set(original_requests.values_list('doctor_id', flat=True))
            ).order_by('last_name'),
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user),
        # Resend the previous inputs of the user
        'values': request.GET
    }
    return render(request, 'pages/opinions_history.html', context)