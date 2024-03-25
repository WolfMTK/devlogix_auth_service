BODY_USER_LOGIN_EXAMPLE = {
    'Get token by username': {
        'summary': 'Get token by username and password',
        'value': {
            'username': 'UserAdmin',
            'password': 'UserAdmin12_'
        }
    },
    'Get token by email': {
        'summary': 'Get token by email and password',
        'value': {
            'email': 'user@mail.com',
            'password': 'UserAdmin12_'
        }
    }
}

RESPONSE_LOGIN_EXAMPLE = {
    200: {
        'description': 'Successful Response',
        'content': {
            'application/json': {
                'example': {
                    'accessToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                                   'eyJzdWIiOiJVc2VyQWRtaW4ifQ.dEo6P6kQwufc0E'
                                   'KNK9c7QTK59yEL-4rUrhVjjkjM4os',
                    'expiresIn': 600,
                    'refreshToken': 'cc9583a2-85d7-504a-b518-b0d86506b749',
                    'tokenType': 'Bearer'
                }
            }
        }
    },
    400: {
        'description': 'Bad Request',
        'content': {
            'application/json': {
                'examples': {
                    'Enter username and email': {
                        'value': {
                            'detail': 'Invalid data received: username and '
                                      'email transmitted at the same time.'
                        }
                    },
                    'The email and username fields are empty': {
                        'value': {
                            'detail': 'Invalid data received: email or '
                                      'username field is empty.'
                        }
                    },
                    'Incorrect data entry': {
                        'value': {
                            'detail': 'The data was entered incorrectly.'
                        }
                    }
                }
            }
        }
    },
}
