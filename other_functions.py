def fix_string(string):
    correct = ''
    for i in string:
        if i == '(' or i == ')' or i == '.' or i == '#' or i == '-':
            correct += '\\'
        correct += i
    return correct


def fix_date(date):
    return fix_string(date[8:10] + '.' + date[5:7] + '.' + date[:4])


def locale_rank(rank):
    if rank == 'newbie':
        return 'новичок'
    if rank == 'pupil':
        return 'ученик'
    if rank == 'specialist':
        return 'специалист'
    if rank == 'expert':
        return 'эксперт'
    if rank == 'candidate master':
        return 'кандидат в мастера'
    if rank == 'master':
        return 'мастер'
    if rank == 'international master':
        return 'международный мастер'
    if rank == 'grandmaster':
        return 'гроссмейстер'
    if rank == 'international grandmaster':
        return 'международный гроссмейстер'
    if rank == 'legendary grandmaster':
        return 'легендарный гроссмейстер'
