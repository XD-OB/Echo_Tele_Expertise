from django import template
from datetime import datetime

register = template.Library()

# register the template filter with django
@register.filter
def to_str(nbr):
    '''
    Convert a int to string
    '''
    return str(nbr)

@register.filter
def get_fullname(user):
    '''
    Return the full name of a person
    '''
    return user.last_name + ' ' + user.first_name

@register.filter
def get_docname(user):
    '''
    Return the full name of a doctor
    '''
    return 'Dr ' + user.last_name + ' ' + user.first_name

@register.filter
def to_whiteescape(mystr):
    '''
    Return the string Capitalized whit 1 whitespace
    '''
    mystr = ' '.join(mystr.split())
    mystr = mystr.capitalize()
    return mystr