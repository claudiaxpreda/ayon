from __future__ import print_function, unicode_literals

import json
import requests
import sys
from settings import URL_SERVER

from clint.textui import colored, puts
from examples import custom_style_3, custom_style_2
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
        values = 'Evenst'
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
            'name': '3. Delete {var}'.format(var=value),
            'value': 'delete'
        },
        Separator(),
        {
            'name': '4. Update {var}'.format(var=value),
            'value': 'update'
        },
        Separator(),
        {
            'name': '5. Go back to menu',
            'value': 'back'
        }
    ]

    question_actions = {
        'type': 'list',
        'name': '{var}'.format(var=answers['menu']),
        'qmark': '😃',
        'message': '',
        'choices': choices
    }
    return (question_actions, answers['menu'])

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
        'name': 'date',
        'message': 'Date:\n Format: YYYY-MM-DD:T22:51:03.494Z',
        'default': 'None'
    },
    # {
    #     'type': 'input',
    #     'name': 'time',
    #     'message': 'Time:\n Format: HH:MM',
    # }
    {
        'type': 'rawlist',
        'name': 'importance',
        'message': 'Importance:',
        'choices': ['Low', 'Medium', 'High', 'None'],
        'filter': lambda val: val.lower()
    }

]
def mange_events_action(base_url,command):
    if command == 'add':
        data = prompt(question_add_event, style=custom_style_2)
        data = {k: v for k, v in data.items() if v.lower() != 'none'}
        # response = s.post('http://localhost:3000/api/users/login', json={'username': 'test', 'password': 'test'})

        response = s.post(base_url, json=data)
        pprint(response.content)
def manage_action(key, command):
    base_url = '{}/{}'.format(URL_SERVER, key)
    mange_events_action(base_url, command[key])

def menu():
    while True:
        data = prompt(question_menu, style=custom_style_2)
        question_actions, key = menu_choices(data)
        if data['menu'] and question_actions:
            data = prompt(question_actions, style=custom_style_2)
            manage_action(key, data)


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
