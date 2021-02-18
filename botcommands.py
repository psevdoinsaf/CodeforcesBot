import requests
from datetime import datetime
from telegram import ParseMode
import json

from other_functions import fix_date, fix_string, locale_rank


def start(update, context):
    update.message.reply_text('Привет, я буду напоминать тебе о раундах и помогу быстро получать полезную информацию!')


def closest_rounds(update, context):
    response = requests.get(url="https://codeforces.com/api/contest.list?gym=false")
    data = response.json()
    if data['status'] != 'OK':
        update.message.reply_text('Произошла ошибка, попробуйте еще раз')
        return
    before = []
    for i in data['result']:
        if i['phase'] == 'BEFORE':
            before.append(i)
        else:
            break
    before.reverse()
    output = ""
    for i in before:
        if i['relativeTimeSeconds'] < -86400 * 7:
            continue
        dt_object = str(datetime.fromtimestamp(i['startTimeSeconds'])).split()
        output += '[' + fix_string(i['name']) + '](https://codeforces.com/contest/' + str(
            i['id']) + ') начнется ' + fix_date(dt_object[0]) + ' в ' + fix_string(dt_object[1][:5])
        output += '\n'
    update.message.reply_text(output, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


def get_user_info(update, context):
    response = requests.get(url="https://codeforces.com/api/user.info?handles=" + ';'.join(context.args))
    data = response.json()
    if data['status'] != 'OK':
        update.message.reply_text('Произошла ошибка, попробуйте еще раз')
        return
    for i in data['result']:
        output = "Хэндл: " + i['handle'] + '\n'
        output += "Рейтинг (максимальный рейтинг), звание: " + str(i['rating']) + ' (' + str(i['maxRating']) + '), ' + \
                  locale_rank(i['rank']) + '\n'
        if 'lastName' in i:
            output += "Фамилия: " + i['lastName'] + '\n'
        if 'firstName' in i:
            output += "Имя: " + i['firstName'] + '\n'
        if 'country' in i:
            output += "Страна: " + i['country'] + '\n'
        if 'city' in i:
            output += "Город: " + i['city'] + '\n'
        if 'organization' in i:
            output += "Организация: " + i['organization'] + '\n'
        update.message.reply_text(output)


def get_contest_standings(update, context):
    round_id = context.args[0]
    handles = context.args[1:]
    response = requests.get(
        url="https://codeforces.com/api/contest.standings?contestId=" + round_id + "&handles=" + ';'.join(
            handles) + "&showUnofficial=true")
    data = response.json()
    if data['status'] != 'OK':
        update.message.reply_text('Произошла ошибка, попробуйте еще раз')
        return
    for i in data['result']['rows']:
        output = "Хэндл: " + i['party']['members'][0]['handle'] + '\nМесто: ' + str(i['rank']) + '\nОчков: ' + \
                 str(int(i['points'])) + '\n'
        problem = 'A'
        for j in i['problemResults']:
            output += problem + ': '
            if j['points'] == 0:
                output += '-'
            else:
                output += '+'
            if j['rejectedAttemptCount']:
                output += str(j['rejectedAttemptCount'])
            output += '\n'
            problem = chr(ord(problem) + 1)
        update.message.reply_text(output)


def get_last_round(update, context):
    response = requests.get(url="https://codeforces.com/api/contest.list?gym=false")
    data = response.json()
    if data['status'] != 'OK':
        update.message.reply_text('Произошла ошибка, попробуйте еще раз')
        return
    for i in data['result']:
        if i['phase'] == 'FINISHED':
            output = i['name'] + ', id: ' + str(i['id'])
            update.message.reply_text(output)
            return
