import sys
from PyInquirer import Separator


UPDATE_EVENTS_OPT = ['Title', 'Description', 'Time', 'Location', 'Importance']
UPDATE_TODOS_OPT = ['Name']
UPDATE_ITEMS_OPT = ['Status']
UPDATE_ACTIVITIES_OPT = ['Steps', 'Kcal', 'Food', 'Date']

question = {
        'type': 'list',
        'name': 'authentification',
        'message': 'Are you already an user?',
           'choices': [ 
            'Login',
            'Register',
            'Exit'
           ]
    }

question_register = [
    {
        'type': 'input',
        'name': 'username',
        'message': 'Username:',
    },
    {
        'type': 'password',
        'name': 'password',
        'message': 'Password:',
    },
    # {
    #     'type': 'input',
    #     'name': 'email',
    #     'message': 'Email:',
    # },
]

question_login = [
    {
        'type': 'input',
        'name': 'username',
        'message': 'Username:',
    },
    {
        'type': 'password',
        'name': 'password',
        'message': 'Password:',
    }
]

question_menu = {
    'type': 'list',
    'name': 'menu',
    'qmark': '😃',
    'message': '',
    'choices': [
        {
            'name': '1. Go to Events',
            'value': 'events'
        },
        Separator(),
        {
            'name': '2. Go to Activities',
            'value': 'activities'
        },
        Separator(),
        {
            'name': '3. Go to Todo Lists',
            'value': 'todos'
        },
        Separator(),
        {
            'name': '4. Exit',
            'value': 'exit'
        }
    ]
}

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
        'when': lambda answers: answers['time'] != 'None',
        'validate': lambda answer: 'Time is required.' \
                if len(answer) == 0 else True
    },
    {
        'type': 'rawlist',
        'name': 'importance',
        'message': 'Importance:',
        'choices': ['Low', 'Medium', 'High', 'None'],
        'filter': lambda val: val.lower()
    }

]

question_add_todo_list = {
    'type': 'input',
    'name': 'title',
    'message': '*Title:',
    'validate': lambda answer: 'Title is required.' \
        if len(answer) == 0 else True
}

question_add_item_list = [
    {
        'type': 'input',
        'name': 'name',
        'message': '*Name:',
        'validate': lambda answer: 'Name is required.' \
            if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'description',
        'message': '*Name:',
    }
]

question_add_activity = [
    {
        'type': 'input',
        'name': 'steps',
        'message': '*Steps:',
        'validate': lambda answer: 'Name is required.' \
            if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'kcal',
        'message': 'Kcal:',
    },
    {
        'type': 'input',
        'name': 'food',
        'message': 'Food list(separate by ,):',
    },
    {
        'type': 'input',
        'name': 'date',
        'message': '*Date YYYY-MM-DD:',
        'validate': lambda answer: 'Date is required.' \
            if len(answer) == 0 else True
    },
]
def getDateTime(date_format):
    date = date_format[:10]
    hour = date_format[11:16]

    return (date, hour)

def get_update_checkbox(items): 
    choices = []
    for item in items:
        choices.append({
            'name': item
        })

    return {
        'type': 'checkbox',
        'name': 'fields_to_update',
        'message': 'Select what fields to update:',
        "choices": choices 
    }

def get_update_question(answer, data):
    question=[]
    for item in answer:
        key = item.lower()

        if key != 'time' and key != 'importance':
            value =  data[key] if key in data.keys() else 'None'
            itemq = {
                'type': 'input',
                'name': key,
                'message': '{}:'.format(item),
                'default': value
            }
            question.append(itemq)
        elif key == 'importance':
            itemq = {
                'type': 'rawlist',
                'name': 'importance',
                'message': 'Importance:',
                'choices': ['Low', 'Medium', 'High', 'None'],
                'filter': lambda val: val.lower()
            }
            question.append(itemq)
        else:
            date, hour = getDateTime(data[key])
            itemq = {
                'type': 'input',
                'name': key,
                'message': 'Date:',
                'default': date
            }
            item_time = {
                'type': 'input',
                'name': 'hour',
                'message': 'Hour:',
                'default': hour,
                'when': lambda answers: answers['time'] != 'None',
                'validate': lambda answer: 'Hour is required.' \
                                if len(answer) == 0 else True
            }
            question.append(itemq)
            question.append(item_time)


    return question


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

def question_items_list(item_list, key):
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