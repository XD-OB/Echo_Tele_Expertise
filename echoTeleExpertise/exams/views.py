from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from mylib.notifications import get_summary_notifs, str_docname, str_fullname
from django.shortcuts import get_object_or_404, render, redirect
from patients.models import Patient, Relation
from .models import Request, Document
from core.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import RequestForm
from django.template.loader import get_template
from echoTeleExpertise.consts import ete_email
from django.contrib import messages
from datetime import datetime
from os.path import basename
from xhtml2pdf import pisa  
from io import BytesIO


# Request Detail:
## combine the old and new description:
def     add_new_description(old_text, expert_comment, new_text):
    new_description = "Ancien description:\n" + old_text + "\n\n"
    if expert_comment != '':
        new_description += "Commantaire de l'expert pour acquérir plus d'informations:\n" + expert_comment + "\n\n"
    new_description += " Nouvelle description:\n" + new_text
    return new_description

def     request_detail(request, request_id):
    req = get_object_or_404(Request, pk=request_id)
    # When the send the infos to complete the request:
    if request.method == 'POST':
        # Get the infos:
        subject = request.POST['subject']
        description = request.POST['description']
        is_urgent = request.POST.get('is_urgent', 'NONE')
        files = request.FILES.getlist('files')
        if subject != '':
            req.subject = subject
        if description:
            req.text_doctor = add_new_description(req.text_doctor, req.text_expert, description)
        if is_urgent == 'URGENT':
            req.is_urgent = True
        else:
            req.is_urgent = False
        # Unmark the seens for both the doctor and the expert
        req.is_expert_visited = False
        req.is_doctor_visited = False
        req.is_incomplete = False
        req.create_date = datetime.now()
        req.notification_date = datetime.now()
        # save the request in the db:
        req.save()
        # Add files and save them:
        files = request.FILES.getlist('new_files')
        for f in files:
            document = Document.objects.create(
                request_id=req,
                file=f,
                name=basename(f.name),
                ext=f.name.rsplit('.', 1)[1]
            )
            # Save the document in db
            document.save()
        # Send the Complete Request Email
        if req.doctor_id.is_enable_mail:
            send_mail(
                # Subject
                'ETE: Vous avez compléter les informations complémentaire demandé',
                # Message
                "Vous avez compléter les informations demandés:\nPar: " + str_docname(req.expert_id) + ".\nA propos le patient: " +  str_fullname(req.patient_id) + ".\nAvec l'objet: " + req.subject  + ".\n- Meryem Rkach",
                # From (Email)
                ## A variable that contain the ete mail
                ete_email,
                # To (Email)
                [req.doctor_id.email, ],
                # If the send fail do not affich any errors
                fail_silently = True
            )
        # Send the Complete Request Email to the Expert
        if req.expert_id.is_enable_mail:
            send_mail(
                # Subject
                "ETE: Un demandeur d'avis d'expertise a complété les informations complémentaire.",
                # Message
                "Des informations complémentaire sont envoyé à propos la demande:\nL'objet: " + req.subject  + ".\nPar: " + str_docname(req.doctor_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                # From (Email)
                ## A variable that contain the ete mail
                ete_email,
                # To (Email)
                [req.expert_id.email, ],
                # If the send fail do not affich any errors
                fail_silently = True
            )
        messages.success(request, 'La completion de la demande est effectuer avec succès.')
        return HttpResponseRedirect('/requests/detail/' + str(request_id))
    # if the request is marked incomplete we should mark it seen
    if req.is_incomplete == True and req.is_doctor_visited == False:
        req.is_doctor_visited = True
        req.save()
    documents = Document.objects.filter(request_id=request_id)
    context = {
        'documents': documents,
        'req': req,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'exams/request.html', context)


# My Solved Request Detail:
def     request_solved_detail(request, req_id):
    req = get_object_or_404(Request, pk=req_id)
    # Mark the solved request as seen
    if req.is_doctor_visited == False:
        req.is_doctor_visited = True
        req.save()
    doctor_documents = Document.objects.filter(request_id=req_id, is_answer=False)
    expert_documents = Document.objects.filter(request_id=req_id, is_answer=True)
    context = {
        'doctor_documents': doctor_documents,
        'expert_documents': expert_documents,
        'req': req,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'exams/request_solved_detail.html', context)


# My Solved Request in PDF:
@login_required
def     get_request_pdf(request, request_id):
    req = get_object_or_404(Request, pk=request_id)
    context = {
        'req': req
    }
    template = get_template('exams/get_request_pdf.html')
    # Render the template
    data_p = template.render(context)
    response=BytesIO()
    pdf_page = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    # If there is no error in pdf Generation, I will show the PDF Page download
    if pdf_page.err:
        return HttpResponse("<h1 style='margin: 5em'>Error dans la generation du pdf</h1>")
    return HttpResponse(response.getvalue(), content_type="application/pdf")


# My Solved Opinion Detail:
@login_required
def     opinion_solved_detail(request, req_id):
    req = get_object_or_404(Request, pk=req_id)
    doctor_documents = Document.objects.filter(request_id=req_id, is_answer=False)
    expert_documents = Document.objects.filter(request_id=req_id, is_answer=True)
    context = {
        'doctor_documents': doctor_documents,
        'expert_documents': expert_documents,
        'req': req,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'exams/opinion_solved_detail.html', context)


# My Solved Opinion in PDF:
@login_required
def     get_opinion_pdf(request, request_id):
    req = get_object_or_404(Request, pk=request_id)
    context = {
        'req': req
    }
    template = get_template('exams/get_opinion_pdf.html')
    # Render the template
    data_p = template.render(context)
    response=BytesIO()
    pdf_page = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    # If there is no error in pdf Generation, I will show the PDF Page download
    if pdf_page.err:
        return HttpResponse("<h1 style='margin: 5em'>Error dans la generation du pdf</h1>")
    return HttpResponse(response.getvalue(), content_type="application/pdf")


# Add New Request
@login_required
def     add_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        # the old values of the request 
        values = request.POST
        if form.is_valid():      
            # Get infos:
            exam_date = request.POST.get('exam_date', datetime.now())
            is_urgent = request.POST.get('is_urgent', 'NONE')
            patient_id = request.POST['patient_id']
            expert_id = request.POST['expert_id']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            # Check if the user choose an expert
            if expert_id == '':
                messages.error(request, "Veuillez selectionner un expert!")
                return redirect('exams:add_request')
            # Check if the user choose an expert
            if patient_id == '':
                messages.error(request, "Veuillez selectionner un patient!")
                return redirect('exams:add_request')
            # Search the instance Expert
            try:
                expert = User.objects.get(pk=expert_id)
            except User.DoesNotExist:
                messages.error(request, "Veuillez selectionner un expert valid!")
                return redirect('exams:add_request')
            # Search the instance Patient
            try:
                patient = Patient.objects.get(pk=patient_id)
            except Patient.DoesNotExist:
                messages.error(request, "Veuillez selectionner un patient valid!")
                return redirect('exams:add_request')
            req = Request.objects.create(
                exam_date=exam_date,
                patient_id=patient,
                doctor_id=request.user,
                expert_id=expert,
                subject=subject,
                text_doctor=description,
            )
            # If urgent change is_urgent to True
            if is_urgent == 'URGENT':
                req.is_urgent = True
            # Save the request in db
            req.save()
            # Iterate in files and save them:
            files = request.FILES.getlist('files')
            for f in files:
                document = Document.objects.create(
                    request_id=req,
                    file=f,
                    name=basename(f.name),
                    ext=f.name.rsplit('.', 1)[1]
                )
                # Save the document in db
                document.save()
            # Send the New Request Email to the Owner
            if req.doctor_id.is_enable_mail:
                send_mail(
                    # Subject
                    "ETE: Votre demande d'avis d'expertise est crée avec succès.",
                    # Message
                    "Votre demande:\nL'objet: " + req.subject  + ".\nL'expert: " + str_docname(req.expert_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                    # From (Email)
                    ## A variable that contain the ete mail
                    ete_email,
                    # To (Email)
                    [req.doctor_id.email, ],
                    # If the send fail do not affich any errors
                    fail_silently = True
                )
            # Send the New Request Email to the Expert
            if req.expert_id.is_enable_mail:
                send_mail(
                    # Subject
                    "ETE: Vous avez recu une nouvelle demande d'avis.",
                    # Message
                    "Le tele-dossier:\nL'objet: " + req.subject  + ".\nDemandeur d'avis: " + str_docname(req.doctor_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                    # From (Email)
                    ## A variable that contain the ete mail
                    ete_email,
                    # To (Email)
                    [req.expert_id.email, ],
                    # If the send fail do not affich any errors
                    fail_silently = True
                )
            messages.success(request, "La nouvelle demande est envoyé")
    else:
        form = RequestForm()
        values = {}
    users = User.objects.exclude(email=request.user.email).exclude(is_staff=True)
    my_relations = Relation.objects.filter(doctor_id__pk=request.user.pk)
    context = {
        'form': form,
        'values': values,
        'doctors': users,
        'relations': my_relations,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'exams/add_request.html', context)


# Add new Request to a specifique doctor
@login_required
def     ask_request(request, expert_id):
    # Search the Expert if not find display 404 Error
    expert = get_object_or_404(User, pk=expert_id)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        # the old values of the request 
        values = request.POST
        if form.is_valid():  
            # Get infos:
            exam_date = request.POST.get('exam_date', datetime.now())
            is_urgent = request.POST.get('is_urgent', 'NONE')
            subject = form.cleaned_data['subject']
            patient_id = form.patient_id
            description = form.cleaned_data['description']
            # Search the instance Patient
            try:
                patient = Patient.objects.get(pk=patient_id)
            except Patient.DoesNotExist:
                messages.error(request, "Veuillez selectionner un patient valid!")
                return redirect('exams:ask_request')
            req = Request.objects.create(
                exam_date=exam_date,
                patient_id=patient,
                doctor_id=request.user,
                expert_id=expert,
                subject=subject,
                text_doctor=description,
            )
            # If urgent change is_urgent to True
            if is_urgent == 'URGENT':
                req.is_urgent = True
            # Save the request in db
            req.save()
            # Iterate in files and save them:
            files = request.FILES.getlist('files')
            for f in files:
                document = Document.objects.create(
                    request_id=req,
                    file=f,
                    name=basename(f.name),
                    ext=f.name.rsplit('.', 1)[1]
                )
                # Save the document in db
                document.save()
            # Send the New Request Email to the Owner
            if request.user.is_enable_mail:
                send_mail(
                    # Subject
                    "ETE: Votre demande d'avis d'expertise est crée avec succès.",
                    # Message
                    "Votre demande:\nL'objet: " + req.subject  + ".\nL'expert: " + str_docname(req.expert_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                    # From (Email)
                    ## A variable that contain the ete mail
                    ete_email,
                    # To (Email)
                    [req.doctor_id.email, ],
                    # If the send fail do not affich any errors
                    fail_silently = True
                )
            # Send the New Request Email to the Expert
            if req.expert_id.is_enable_mail:
                send_mail(
                    # Subject
                    "ETE: Vous avez recu une nouvelle demande d'avis.",
                    # Message
                    "Le tele-dossier:\nL'objet: " + req.subject  + ".\nDemandeur d'avis: " + str_docname(req.doctor_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                    # From (Email)
                    ## A variable that contain the ete mail
                    ete_email,
                    # To (Email)
                    [req.expert_id.email, ],
                    # If the send fail do not affich any errors
                    fail_silently = True
                )
            messages.success(request, "La nouvelle demande est envoyé au Dr " + expert.last_name + " " + expert.first_name)
    else:
        form = RequestForm()
        values = {}
    my_relations = Relation.objects.filter(doctor_id__pk=request.user.pk)
    context = {
        'form': form,
        'values': values,
        'expert': expert,
        'relations': my_relations,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'exams/ask_request.html', context)


# Add New Request to a specifique patient
@login_required
def     patient_request(request, patient_id):
    # Search the Patient if not find display 404 Error
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        # the old values of the request 
        values = request.POST
        if form.is_valid():      
            # Get infos:
            exam_date = request.POST.get('exam_date', datetime.now())
            is_urgent = request.POST.get('is_urgent', 'NONE')
            expert_id = request.POST['expert_id']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            # Test Expert id:
            if expert_id == '':
                messages.error(request, "Veuillez selectionner un expert valid!")
                return redirect('exams:patient_request', patient_id)
            # Search the instance Expert
            try:
                expert = User.objects.get(pk=expert_id)
            except User.DoesNotExist:
                messages.error(request, "Veuillez selectionner un expert valid!")
                return redirect('exams:patient_request', patient_id)
            req = Request.objects.create(
                exam_date=exam_date,
                patient_id=patient,
                doctor_id=request.user,
                expert_id=expert,
                subject=subject,
                text_doctor=description,
            )
            # If urgent change is_urgent to True
            if is_urgent == 'URGENT':
                req.is_urgent = True
            # Save the request in db
            req.save()
            # Iterate in files and save them:
            files = request.FILES.getlist('files')
            for f in files:
                document = Document.objects.create(
                    request_id=req,
                    file=f,
                    name=basename(f.name),
                    ext=f.name.rsplit('.', 1)[1]
                )
                # Save the document in db
                document.save()
            # Send the New Request Email to the Owner
            if req.doctor_id.is_enable_mail:
                send_mail(
                    # Subject
                    "ETE: Votre demande d'avis d'expertise est crée avec succès.",
                    # Message
                    "Votre demande:\nL'objet: " + req.subject  + ".\nL'expert: " + str_docname(req.expert_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                    # From (Email)
                    ## A variable that contain the ete mail
                    ete_email,
                    # To (Email)
                    [req.doctor_id.email, ],
                    # If the send fail do not affich any errors
                    fail_silently = True
                )
            # Send the New Request Email to the Expert
            if req.expert_id.is_enable_mail:
                send_mail(
                    # Subject
                    "ETE: Vous avez recu une nouvelle demande d'avis.",
                    # Message
                    "Le tele-dossier:\nL'objet: " + req.subject  + ".\nDemandeur d'avis: " + str_docname(req.doctor_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                    # From (Email)
                    ## A variable that contain the ete mail
                    ete_email,
                    # To (Email)
                    [req.expert_id.email, ],
                    # If the send fail do not affich any errors
                    fail_silently = True
                )
            messages.success(request, "La nouvelle demande est envoyé")
            return redirect('pages:list_patients')
    else:
        form = RequestForm()
        values = {}
    users = User.objects.exclude(email=request.user.email).exclude(is_staff=True)
    context = {
        'form': form,
        'values': values,
        'patient': patient,
        'doctors': users,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'exams/patient_request.html', context)


@login_required
def     mark_incomplete(request, request_id):
    '''
    Mark the request as Incomplet
    Mark only if the request method is POST !
    '''
    if request.method == 'POST':
        try:
            req = Request.objects.get(
                pk=request_id,
                expert_id=request.user
            )
        except Request.DoesNotExist:
            raise Http404("Request Failed!")
        # Add the comment send by the expert in text_expert field
        if 'text_expert' in request.POST:
            comment = request.POST['text_expert']
            if comment:
                req.text_expert = comment
        req.is_incomplete = True
        # Unmark the visited for the owner of the request to resee the request
        req.is_doctor_visited = False
        req.notification_date = datetime.now()
        req.save()
        # Send the Request Incomplet Email to the Owner
        if req.doctor_id.is_enable_mail:
            send_mail(
                # Subject
                "ETE: D'après l'expert votre demande d'avis d'expertise nécessite des informayions complémentaire.",
                # Message
                "Votre demande est incomplete:\nL'objet: " + req.subject  + ".\nL'expert: " + str_docname(req.expert_id) + ".\nLe patient: " +  str_fullname(req.patient_id) + ".\n- Meryem Rkach",
                # From (Email)
                ## A variable that contain the ete mail
                ete_email,
                # To (Email)
                [req.doctor_id.email, ],
                # If the send fail do not affich any errors
                fail_silently = True
            )
        messages.success(request, 'Une demande des informations complémentaire est envoyé au Dr ' + req.doctor_id.last_name + ' ' + req.doctor_id.first_name + '.')
        return redirect('pages:telefiles')
    return HttpResponseNotAllowed('Not allowed to go to this page')


@login_required
def     mark_paid(request, request_id):
    '''
    Mark the request as Paid
    '''
    req = get_object_or_404(Request, pk=request_id)
    req.is_paid = True
    req.save()
    return redirect('exams:request_solved_detail', request_id)