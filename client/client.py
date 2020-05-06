from __future__ import print_function, unicode_literals

import json
import requests

from settings import URL_SERVER
from clint.textui import colored, puts, indent
from examples import custom_style_3, custom_style_2, custom_style_1
from PyInquirer import (
    style_from_dict,
    Token, 
    prompt,
    Validator,
    ValidationError,
    Separator
)
from pprint import pprint
from questions import *

s = requests.Session()

def print_event_data(event):
    keys = event.keys()

    if 'time' in keys:
        date = '{}/{}'.format(event['time'][:10],\
                                    event['time'][11:16])
    else:
        date = None
    with indent(6, quote='  >'):
        puts(colored.green('Title: ', bold=True) + event['title'])
        puts(colored.green('Description: ', bold=True) + event['description'])
        puts(colored.green('Date: ', bold=True) + (date if date else 'No date provided'))
        puts(colored.green('Location: ', bold=True) + (event['location']\
                if 'location' in keys else 'No location provided'))
        puts(colored.green('Importance: ', bold=True) + (event['importance']\
                if 'importance' in keys else 'No importance provided'))

def print_todos_data(todo):
    keys = todo.keys()

    if 'time' in keys:
        date = '{}/{}'.format(event['time'][:10],\
                              event['time'][11:16])
    else:
        date = None
    with indent(6, quote='  >'):
        puts(colored.magenta('Title: ', bold=True) + todo['title'])

        puts(colored.blue('Items:'))
        with indent(8, quote='  >'):
            for item in todo['items']:
                keys = item.keys()
                puts(colored.magenta('Name: ', bold=True) + (item['name']\
                    if 'name' in keys else 'No name provided'))
                puts(colored.magenta('Status: ', bold=True) + (item['done']\
                    if 'done' in keys else 'No status provided'))

def print_activities_data(event):
    keys = event.keys()

    if 'date' in keys:
        date = '{}/{}'.format(event['date'][:10],\
                                    event['date'][11:16])
    else:
        date = None
    with indent(6, quote='  >'):
        puts(colored.green('Activity Date: ', bold=True) + (date if date else 'No date provided'))
        puts(colored.green('Steps: ', bold=True) + (event['steps']\
                if 'steps' in keys else 'No value provided'))
        puts(colored.green('Kcals: ', bold=True) + (event['kcal']\
                if 'kcal' in keys else 'No value provided'))
        puts(colored.green('Food: ', bold=True) + (event['food']\
                if 'food' in keys else 'No food provided'))

def getRequest(base_url):
    response = s.get(base_url)
    if response.status_code != 200:
        puts(colored.red('Something went wrong', bold=True))
        return []
    return json.loads(response.content.decode('utf-8'))

def postRequest(base_url, data):
    response = s.post(base_url, json=data)
    return response.content.decode('utf-8')

def getByIdRequest(base_url, id):
    response = s.get('{}/{}'.format(base_url, id))
    if response.status_code != 200:
        puts(colored.red('Something went wrong', bold=True))
        return None
    return json.loads(response.content.decode('utf-8'))

def deleteById(base_url, id):
    response = s.delete('{}/{}'.format(base_url, id))
    return response.content.decode('utf-8')

def updateById(base_url, id, data):
    response = s.put('{}/{}'.format(base_url, id), json=data)
    return response.content.decode('utf-8')

def dateFormat(data):
    data['time'] = '{}T{}:00.000Z'.format(data['time'], data['hour'])
    del data['hour']

    return data

def get_questions_item(key):
    if key == 'events':
        return (question_add_event, print_event_data, UPDATE_EVENTS_OPT, 'title')
    
    if key == 'todolists':
        return (question_add_todo_list ,print_todos_data, UPDATE_TODOS_OPT, 'title')
    
    if key == 'items':
        return (question_add_items_list, print_todos_data, UPDATE_ITEMS_OPT, 'name')
    
    return (question_add_activity, print_activities_data, UPDATE_ACTIVITIES_OPT, 'date')

def mange_item_action(base_url,command, key, single_q):
    question_add,print_function, option_update, field = get_questions_item(key)

    if command == 'add':
        data = prompt(question_add, style=custom_style_2)
        data = {k: v for k, v in data.items() if v.lower() != 'none'}

        if 'hour' in data.keys():
            data = dateFormat(data)
        response = postRequest(base_url, data)
        puts(colored.red(response, bold=True))

    if command == 'list':
        items_list = getRequest(base_url)

        while True:
            items_question = question_items_list(items_list, field)
            item = prompt(items_question, style=custom_style_2)

            if item['list'] != 'back':
                while True:
                    data = getByIdRequest(base_url, item['list'])
                    if data == None:
                        continue
                    print_function(data)
                    answer = prompt(single_q, style=custom_style_2)

                    if answer[key] != 'update' and answer[key] != 'additem':
                        if answer[key] == 'delete':
                            response = deleteById(base_url, item['list'])
                            puts(colored.red(response, bold=True))
                            items_list = getRequest(base_url)
                        break
                    if answer[key] == 'update':
                        answer_u = prompt(get_update_checkbox(option_update), style=custom_style_2)
                        pprint(answer_u)
                        data = prompt(get_update_question(answer_u['fields_to_update'], data), 
                                                                    style=custom_style_3)

                        if 'hour' in data.keys():
                            dateFormat(data)
                        response = updateById(base_url, item['list'], data)
                        puts(colored.red(response, bold=True))

                    if answer[key] == 'additem':
                        idata = prompt(question_add_item_list, style=custom_style_2)
                        url_item = '{}/{}'.format(base_url, item['list'])
                        response = updateById(url_item,'item', idata)
                        puts(colored.red(response, bold=True))


            else:
                manage_action({'menu': key})

    if command == 'back':
        menu()


def manage_action(data):
    question_actions, single_q, key = menu_choices(data)
    while True:
        command = prompt(question_actions, style=custom_style_2)
        base_url = '{}/{}'.format(URL_SERVER, key)
        mange_item_action(base_url, command[key], key, single_q)

def menu():
    url_reminder = '{}/users/reminder'.format(URL_SERVER)
    while True:
        data = prompt(question_menu, style=custom_style_2)
        if data['menu'] != 'reminder':
            manage_action(data)
        else:
            response = postRequest(url_reminder, data={})
            puts(colored.red(response, bold=True))


def login():
    url_log = '{}/users/login'.format(URL_SERVER)
    data = prompt(question_login, style=custom_style_3)
    response = s.post(url_log, json=data)

    if response.status_code == 200:
        puts(colored.magenta("Go to menu", bold=True))
        menu()
    else:
        message = response.content.decode('utf-8')
        puts(colored.red(message, bold=True))
        main()

def register():
    data = prompt(question_register, style=custom_style_2)
    url_reg = '{}/users/register'.format(URL_SERVER)
    response = requests.post(url_reg, json=data)
    return response

def main():
    puts(colored.magenta("Welcome to your daily planner", bold=True))
    answers = prompt(question, style=custom_style_3)
    if answers['authentification'] == 'Register':
        response = register()
        if response.status_code == 200:
            puts(colored.magenta("Go to login", bold=True))
            login()
        else:
            message = response.content.decode('utf-8')
            puts(colored.red(message, bold=True))
            main()
    elif answers['authentification'] == 'Login':
        login()
    else:
        return

if __name__ == "__main__":
    main()
