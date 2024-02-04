BODY_USER_CREATE_EXAMPLE = {
    'username': 'UserAdmin',
    'email': 'user@mail.com',
    'password': 'UserAdmin12_'
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
                'examples': {
                    'Invalid Username': {
                        'value': {'detail': 'Пользователь с таким юзернеймом уже существует!'}
                    },
                    'Invalid Email': {
                        'value': {'detial': 'Пользователь с такой почтой уже существует!'}
                    }
                }
            }
        }
    },
}

RESPONSE_LOGIN_EXAMPLE = {
    200: {
        'content': {
            'application/json': {
                'example': {
                    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJVc2VyQWRtaW4iLCJkYXRlIjoiMjAyNC0wMi0wNCAxNzozOToxMC43NjI1NzMiLCJleHAiOjE3MDcwNTc1NTB9.utFkx8oFaTEYfDStUmQV2lM7yK51IK87cjxVbqZCk0k',
                    'expires_in': 600,
                    'refresh_token': 'cc9583a2-85d7-504a-b518-b0d86506b749',
                    'token_type': 'Bearer'
                }
            }
        }
    }
}

RESPONSE_USER_GET_EXAMPLE = {
    200: {
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
}

RESPONSE_LOGOUT_EXAMPLE = {
    204: {
        'content': None
    }
}
