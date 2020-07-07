def str_fullname(user):
    '''
    Return the full name of a person
    '''
    return user.last_name + ' ' + user.first_name


def str_docname(user):
    '''
    Return the full name of a doctor
    '''
    return 'Dr ' + user.last_name + ' ' + user.first_name