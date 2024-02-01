BODY_USER_CREATE_EXAMPLE = {
    'username': 'UserAdmin',
    'email': 'user@mail.com',
    'password': 'UserAdmin12'
}

RESPONSE_USER_CREATE_EXAMPLE = {
    201: {
        'content': {'application/json':
            {
                'example': {
                    'id': 1,
                    'username': 'UserAdmin',
                    'email': 'user@mail.com',
                    'is_active': True
                }
            }
        }
    },
    404: {
        'content': {'application/json':
            {
                'example': {
                    'detail': 'The user already exists!'
                }
            }
        }
    },
}
