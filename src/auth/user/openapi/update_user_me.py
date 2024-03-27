BODY_USER_UPDATE_ME_EXAMPLE = {
    'username': 'UserAdmin',
    'email': 'user@mail.com',
    'password': 'UserAdmin12_'
}

RESPONSE_USER_UPDATE_ME_EXAMPLE = {
    200: {
        'description': 'Successful Response',
        'content': {
            'application/json': {
                'example': {
                    'id': 'ba394529-3dcd-4a46-9534-895b5a0cbf3b',
                    'username': 'UserAdmin',
                    'email': 'user@mail.com',
                }
            }
        }
    },
    400: {
        'description': 'Bad Request',
        'content': {
            'application/json': {
                'examples': {
                    'Invalid Email': {
                        'value': {
                            'detail': 'A user with this E-mail already '
                                      'exists.'
                        }
                    },
                    'Invalid username': {
                        'value': {
                            'detial': 'A user with this username already '
                                      'exists.'
                        }
                    },
                }
            }
        }
    },
    422: {
        'description': 'Unprocessable Entity',
        'content': {
            'application/json': {
                'examples': {
                    'Length Email': {
                        'value': {
                            'detail': 'The allowed length for E-mail is '
                                      'exceeded.'
                        }
                    },
                    'Invalid Email': {
                        'value': {
                            'detail': 'The value for the email field is '
                                      'invalid.'
                        }
                    }
                }
            }
        }
    }
}
