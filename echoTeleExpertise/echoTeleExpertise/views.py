from django.contrib.auth.decorators import login_required
from mylib.notifications import get_complet_notifs, get_summary_notifs
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mylib.crypt import decrypt_val
from core.models import User
from re import search

# Home page View:
def     index(request):
    # The 3 doctors that have the most opinion given in this app
    top_members = User.objects.filter(is_staff=False).order_by('-count_opinion')[:3]
    context = {
        'doctors': top_members,
        # Get the summary of notifications via the fonction
        'notifications': get_summary_notifs(request.user)
    }
    return render(request, 'echoTeleExpertise/index.html', context)


# Notification listing View
@login_required
def     news(request):
    '''
    View used to list the notifications
    '''
    notifications = get_complet_notifs(request.user)
    # Mark the notifications visited:
    if request.method == 'POST':
        for req in notifications['complet']:
            if req.doctor_id == request.user:
                req.is_doctor_visited = True
            else:
                req.is_expert_visited = True
            req.save()
        return redirect('news')
    # Mark the Vues seen
    notifications['complet'].filter(
        doctor_id = request.user,
        is_incomplete = False,
        is_close = False
    ).update(is_doctor_visited=True)
    context = {
        'notifications': notifications
    }
    return render(request, 'echoTeleExpertise/notifications.html', context)


def      activate_account(request, hash_code):
    '''
    Activate the accout
    '''
    decrypted_code = decrypt_val(bytes(hash_code, encoding='utf-8'))
    user = get_object_or_404(User, email=decrypted_code)
    user.is_verified_mail = True
    user.save()
    messages.success(request, 'Votre email est verifié vous pouvez se connecter à votre compte')
    return render(request, 'accounts/login.html', {})


def      change_password(request, hash_code):
    '''
    Change password of the account
    '''
    decrypted_code = decrypt_val(bytes(hash_code, encoding='utf-8'))
    user = get_object_or_404(User, email=decrypted_code)
    if request.POST == 'POST':
        # Get the passwords:
        password = request.POST['password']
        password2 = request.POST['password2']
        # If the 2 passwords empty
        if password == '' or password2 == '':
            messages.error(request, 'Un des champs est Vide!')
            return redirect('accounts:change_password')
        # Check if the password match requierements:
        # If the 2 passwords match
        if password == password2:
            if ((len(password) < 8) or (search('[0-9]', password) is None) or (search('[A-Z]', password) is None)):
                messages.warning(request, 'Veuillez utilisé un mot de passe fort (conbinaison de chiffres et lettres) avec une longueur qui dépasse 8 caractères!')
                return redirect('accounts:change_password')
            # Change the passwords
            user.set_password(password)
            user.save()
            messages.success(request, 'Votre mot de passe a été changer avec succès.')
            
            return redirect('accounts:login')
        messages.error(request, 'Les deux mots de passe ne se match pas!')
    return render(request, 'accounts/change_password.html', {})