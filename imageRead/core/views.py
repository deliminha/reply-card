def not_in_student_group(user):
    if user:
        return user.groups.filter(name='Estudante').count() == 0
    return False


def not_in_teacher_group(user):
    if user:
        return user.groups.filter(name='Professor').count() == 0
    return False


def not_in_coordinator_group(user):
    if user:
        return user.groups.filter(name='Coordenador').count() == 0
    return False


def not_in_manager_group(user):
    if user:
        return user.groups.filter(name='Administrador').count() == 0
    return False
