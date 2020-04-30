from __future__ import print_function, unicode_literals

import json
import requests
#import sys
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


def getRequest(base_url):
    response = s.get(base_url)
    return json.loads(response.content.decode('utf-8'))

def postRequest(base_url, data):
    response = s.post(base_url, json=data)
    return response.content.decode('utf-8')

def getByIdRequest(base_url, id):
    response = s.get('{}/{}'.format(base_url, id))
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



def mange_item_action(base_url,command, key, single_q):
    if command == 'add':
        if key == 'events':
            data = prompt(question_add_event, style=custom_style_2)
            data = {k: v for k, v in data.items() if v.lower() != 'none'}
            if 'hour' in data.keys():
                data = dateFormat(data)
            pprint(data)
            response = postRequest(base_url, data)
            puts(colored.red(response))

    if command == 'list' and key == 'events':
        items_list = getRequest(base_url)
        while True:
            # Method for generate question item
            items_question = question_items_list(items_list, 'title')
            item = prompt(items_question, style=custom_style_2)
            if item['list'] != 'back':
                while True:
                    data = getByIdRequest(base_url, item['list'])
                    print_event_data(data)
                    answer = prompt(single_q, style=custom_style_2)

                    if answer[key] is not 'update':
                        if answer[key] is 'delete':
                            response = deleteById(base_url, item['list'])
                            puts(colored.red(response))
                            events_list = getRequest(base_url)
                        break

                    answer = prompt(get_update_checkbox(UPDATE_EVENTS_OPT), style=custom_style_2)
                    data = prompt(get_update_question(answer['fields_to_update'], data), style=custom_style_3)
                    if 'hour' in data.keys():
                        dateFormat(data)
                    response = updateById(base_url, item['list'], data)
                    puts(response)
                    pprint(answer)

            else:
                manage_action({'menu': key})
        if command == 'list' and key == 'todos':
            items_list = getRequest(  base_url = '{}/{}'.format(URL_SERVER, key))



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
