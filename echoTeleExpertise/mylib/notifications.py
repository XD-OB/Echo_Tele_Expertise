from echoTeleExpertise.consts import notifications_max
from exams.models import Request
from django.db.models import Q

def        get_complet_notifs(user):
    '''
    This function return all the unvisited requests
    '''
    if not user.is_authenticated:
        return None
    list_notifications = Request.objects.filter(
        # The new telefiles
        Q(
            is_expert_visited=False,
            is_close=False,
            is_incomplete=False,
            expert_id=user
        ) | 
        # The new incomplete requests
        Q (
            is_doctor_visited=False,
            is_incomplete=True,
            doctor_id=user
        ) | 
        # The new solved requests
        Q (
            is_doctor_visited=False,
            is_close=True,
            doctor_id=user
        ) |
        # The requests saw by the experts:
        Q (
            is_expert_visited=True,
            is_doctor_visited=False,
            is_incomplete=False,
            is_close=False,
            doctor_id=user
        )
    ).order_by('-notification_date')
    notifications = {
        'complet': list_notifications,
        'summary': list_notifications[:notifications_max],
        'len': len(list_notifications)
    }
    return notifications

def        get_summary_notifs(user):
    '''
    This function is used to get the unvisited requests in a dictionary
    '''
    if not user.is_authenticated:
        return None
    len = Request.objects.filter(
        # The new telefiles
        Q(
            is_expert_visited=False,
            is_close=False,
            is_incomplete=False,
            expert_id=user
        ) | 
        # The new incomplete requests
        Q (
            is_doctor_visited=False,
            is_incomplete=True,
            doctor_id=user
        ) | 
        # The new solved requests
        Q (
            is_doctor_visited=False,
            is_close=True,
            doctor_id=user
        ) |
        # The requests saw by the experts:
        Q (
            is_expert_visited=True,
            is_doctor_visited=False,
            is_incomplete=False,
            is_close=False,
            doctor_id=user
        )
    ).count()
    list_notifications = Request.objects.filter(
        # The new telefiles
        Q(
            is_expert_visited=False,
            is_close=False,
            is_incomplete=False,
            expert_id=user
        ) | 
        # The new incomplete requests
        Q (
            is_doctor_visited=False,
            is_incomplete=True,
            doctor_id=user
        ) | 
        # The new solved requests
        Q (
            is_doctor_visited=False,
            is_close=True,
            doctor_id=user
        ) |
        # The requests saw by the experts:
        Q (
            is_expert_visited=True,
            is_doctor_visited=False,
            is_incomplete=False,
            is_close=False,
            doctor_id=user
        )
    ).order_by('-notification_date')[:notifications_max]
    notifications = {
        'summary': list_notifications,
        'len': len 
    }
    return notifications

def str_fullname(user):
    return user.last_name + ' ' + user.first_name

def str_docname(user):
    return 'Dr ' + user.last_name + ' ' + user.first_name
