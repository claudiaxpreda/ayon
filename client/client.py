from __future__ import print_function, unicode_literals

import json
import requests
import sys
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

pprint(URL_SERVER)
s = requests.Session()

def menu_choices(answers):
    choices = []
    value = ''
    values = ''
    if answers['menu'] == 'events':
        value = 'Event'
        values = 'Events'
    elif answers['menu'] == 'activities':
        value = 'Activity'
        values = 'Activities'
    elif answers['menu'] == 'todos':
        value = 'Todo List'
        values = 'Todo Lists'
    else:
        sys.exit()


    choices = [
        {
            'name': '1. Add {var}'.format(var=value),
            'value': 'add'
        },
        Separator(),
        {
            'name': '2. See {var}'.format(var=values),
            'value': 'list'
        },
        Separator(),
        {
            'name': '3. Go back to menu',
            'value': 'back'
        }
    ]

    single_choices = [
        Separator(),
        {
            'name': '1. Update {var}'.format(var=value),
            'value': 'update'
        },
        Separator(),
        {
            'name': '2. Delete {var}'.format(var=value),
            'value': 'delete'
        },
        Separator(),
        {
            'name': '3. Go back to {} list'.format(values),
            'value': 'back'
        },
    ]

    question_single = {
        'type': 'list',
        'name': '{var}'.format(var=answers['menu']),
        'qmark': '😃',
        'message': '',
        'choices': single_choices
    }
    question_actions = {
        'type': 'list',
        'name': '{var}'.format(var=answers['menu']),
        'qmark': '😃',
        'message': '',
        'choices': choices
    }
    return (question_actions, question_single, answers['menu'])

question_add_event = [
        
    {
        'type': 'input',
        'name': 'title',
        'message': '*Title:',
        'validate': lambda answer: 'Title is required.' \
            if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'description',
        'message': '*Description:',
        'validate': lambda answer: 'Description is required.' \
            if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'location',
        'message': 'Location:',
        'default': 'None'
    },
    {
        'type': 'input',
        'name': 'time',
        'message': 'Date:\n Format: YYYY-MM-DD',
        'default': 'None',
        'validate': lambda answer: 'Description is required.' \
            if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'hour',
        'message': 'Time:\n Format: HH:MM',
        'when': lambda answers: answers['time'] != 'None'
    },
    {
        'type': 'rawlist',
        'name': 'importance',
        'message': 'Importance:',
        'choices': ['Low', 'Medium', 'High', 'None'],
        'filter': lambda val: val.lower()
    }

]


def question_events_list(item_list, key):
    choices = [Separator('')]
    itemq = {
        'name': 'Go back',
        'value': 'back'
    }
    choices.append(itemq)
    choices.append(Separator())

    for item in item_list:
        itemq = {
            'name': '{}'.format(item[key]),
            'value': '{}'.format(item['_id'])
        }
        choices.append(itemq)
        choices.append(Separator())

    question = {
        'type': 'list',
        'name': 'list',
        'qmark': '😃',
        'message': 'Events by name',
        'choices': choices
    }
    return question

def print_event_data(event):
    keys = event.keys()

    if 'time' in keys:
        date = '{}/{}'.format(event['time'][:9],\
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

def mange_item_action(base_url,command, item, single_q):
    events = {}

    if command == 'add':
        if item is 'events':
            data = prompt(question_add_event, style=custom_style_2)
            data = {k: v for k, v in data.items() if v.lower() != 'none'}
            if 'hour' in data.keys():
                data['time'] = '{}T{}:00.000Z'.format(data['time'], data['hour'])
                del data['hour']
            response = s.post(base_url, json=data)
            puts(colored.red(response.content.decode('utf-8')))
    if command == 'list':
        response = s.get(base_url)
        events_list = json.loads(response.content.decode('utf-8'))
        while True:
            events_question = question_events_list(events_list, 'title')
            event = prompt(events_question, style=custom_style_2)
            if event['list'] is not 'back':
                while True:
                    response = s.get('{}/{}'.format(base_url, event['list']))
                    data =json.loads( response.content.decode('utf-8'))
                    print_event_data(data)
                    answer = prompt(single_q, style=custom_style_2)
                    #break
                    if answer[item] is not 'update':
                        if answer[item] is 'delete':
                            response = s.delete('{}/{}'.format(base_url, event['list']))
                            puts(colored.red(response.content.decode('utf-8')))
                            response = s.get(base_url)
                            events_list = json.loads(response.content.decode('utf-8'))
                        break
            else:
                manage_action({'menu': item})
        if command == 'back':
            menu()

def mange_todos_action(base_url, command):
    pass

def mange_actions_action(base_url, command):
    pass


def manage_action(data):
    question_actions, single_q, key = menu_choices(data)
    command = prompt(question_actions, style=custom_style_2)

    base_url = '{}/{}'.format(URL_SERVER, key)
    mange_item_action(base_url, command[key], key, single_q)

def menu():
    while True:
        data = prompt(question_menu, style=custom_style_2)
        if data['menu']:
            manage_action(data)


def login():
    data = prompt(question_login, style=custom_style_3)
    response = s.post('http://localhost:3000/api/users/login', json=data)
    if response.status_code == 200:
        menu()
    else:
        pprint('Some error occured')


def register():
    data = prompt(question_register, style=custom_style_2)
    response = requests.post('http://localhost:3000/api/users/register', json=data)
    return response.status_code

def main():
    print("Welcome to your daily planner\n")
    answers = prompt(question, style=custom_style_3)
    if answers['authentification'] == 'Register':
        response = register()
        if response == 200:
            login()
        else:
            pprint('Some error occured')
    elif answers['authentification'] == 'Login':
        login()
    else:
        return

if __name__ == "__main__":
    main()
