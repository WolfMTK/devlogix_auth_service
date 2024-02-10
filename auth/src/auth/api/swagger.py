# flake8 ignore
# noqa

BODY_USER_CREATE_EXAMPLE = {
    'username': 'UserAdmin',
    'email': 'user@mail.com',
    'password': 'UserAdmin12_'
}

RESPONSE_USER_CREATE_EXAMPLE = {
    201: {
        'content': {
            'application/json': {
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
        'content': {
            'application/json': {
                'examples': {
                    'Юзернейм': {
                        'value': {
                            'detail': 'Пользователь с таким юзернеймом уже существует!'
                        }
                    },
                    'Почта': {
                        'value': {
                            'detial': 'Пользователь с такой почтой уже существует!'
                        }
                    },
                }
            }
        }
    },
    422: {
        'content': {
            'application/json': {
                'examples': {
                    'Невалидный E-mail (отсутствие "@")': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'value is not a valid email address: '
                                           'The email address is not valid. '
                                           'It must have exactly one @-sign.'
                                }
                            ]
                        }
                    },
                    'Невалидный E-mail (отсутствие точки в конце)': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'value is not a valid email address: '
                                           'The part after the @-sign is not valid. '
                                           'It should have a period.'
                                }
                            ]
                        }
                    },
                    'Невалидный E-mail': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'value is not a valid email address: '
                                           'There must be something before the @-sign.'
                                }
                            ]
                        }
                    },
                    'Длина почты меньше 6 символов': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'Value should have at least 6 items after validation, not 5'
                                }
                            ]
                        }
                    },
                    'Длина почты больше 191 символ': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'value is not a valid email address: '
                                           'The email address is too long before the @-sign '
                                           '(191 characters too many).'
                                }
                            ]
                        }
                    },
                    'Длина пароля': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'Длина пароля меньше 8 символов.'
                                }
                            ]
                        }
                    },
                    'Невалидный пароль': {
                        'value': {
                            'detaiil': [
                                {
                                    'msg': 'Пароль должен содержать: '
                                           'минимум одну цифру; '
                                           'по крайней мере один алфавит верхнего регистра; '
                                           'по крайней мере один алфавит нижнего регистра; '
                                           'по крайней мере один специальный символ, '
                                           'который включает в себя !#$%&()*+,-./:;<=>?@[\]^_`{|}~.'
                                }
                            ]
                        }
                    },
                    'Длина юзернейма': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'Юзернейм меньше 6 символов.'
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
}

# RESPONSE_LOGIN_EXAMPLE = {
#     200: {
#         'content': {
#             'application/json': {
#                 'example': {
#                     'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJVc2VyQWRtaW4iLCJkYXRlIjoiMjAyNC0wMi0wNCAxNzozOToxMC43NjI1NzMiLCJleHAiOjE3MDcwNTc1NTB9.utFkx8oFaTEYfDStUmQV2lM7yK51IK87cjxVbqZCk0k',
#                     'expires_in': 600,
#                     'refresh_token': 'cc9583a2-85d7-504a-b518-b0d86506b749',
#                     'token_type': 'Bearer'
#                 }
#             }
#         }
#     }
# }
#
# RESPONSE_USER_GET_EXAMPLE = {
#     200: {
#         'content': {'application/json':
#             {
#                 'example': {
#                     'id': 1,
#                     'username': 'UserAdmin',
#                     'email': 'user@mail.com',
#                     'is_active': True
#                 }
#             }
#         }
#     },
# }
#
# RESPONSE_LOGOUT_EXAMPLE = {
#     204: {
#         'content': None
#     }
# }
