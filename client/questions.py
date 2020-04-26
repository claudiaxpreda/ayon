from PyInquirer import Separator

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
