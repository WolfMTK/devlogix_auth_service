RESPONSE_LOGIN_EXAMPLE = {
    200: {
        'description': 'Данные успешно получены',
        'content': {
            'application/json': {
                'example': {
                    'accessToken':
                        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                        '.eyJzdWIiOiJVc2VyQWRtaW4iLCJkYXRlIjoiMjAyNC0wMi0wNCAxNzozOToxMC43NjI1NzMiLCJleHAiOjE3MDcwNTc1NTB9.utFkx8oFaTEYfDStUmQV2lM7yK51IK87cjxVbqZCk0k',
                    'expiresIn': 600,
                    'refreshToken': 'cc9583a2-85d7-504a-b518-b0d86506b749',
                    'tokenType': 'Bearer'
                }
            }
        }
    },
    400: {
        'description': 'Ошибка запроса',
        'content': {
            'application/json': {
                'examples': {
                    'Введен юзернейм и почта': {
                        'value': {
                            'detail': 'Введите username или email.'
                        }
                    },
                    'Отсутствует username': {
                        'value': {
                            'detail': 'Отсутствует username или email.'
                        }
                    },
                    'Отсутствует email': {
                        'value': {
                            'detail': 'Отсутствует username или email'
                        }
                    },
                    'Неверно введены данные': {
                        'value': {
                            'detail': 'Пароль или логин введен неверно.'
                        }
                    }
                }
            }
        }
    },
    422: {
        'description': 'Невалидные данные',
        'content': {
            'application/json': {
                'examples': {
                    'Невалидный E-mail (отсутствие "@")': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'value is not a valid email '
                                           'address: '
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
                                    'msg': 'value is not a valid email '
                                           'address: '
                                           'The part after the @-sign is '
                                           'not valid. '
                                           'It should have a period.'
                                }
                            ]
                        }
                    },
                    'Невалидный E-mail': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'value is not a valid email '
                                           'address: '
                                           'There must be something before '
                                           'the @-sign.'
                                }
                            ]
                        }
                    },
                    'Длина почты меньше 6 символов': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'Value should have at least 6 '
                                           'items after validation, not 5'
                                }
                            ]
                        }
                    },
                    'Длина почты больше 191 символ': {
                        'value': {
                            'detail': [
                                {
                                    'msg': 'value is not a valid email '
                                           'address: '
                                           'Length must not exceed 2048 '
                                           'characters'
                                }
                            ]
                        }
                    },
                }
            }
        }
    }
}

RESPONSE_LOGOUT_EXAMPLE = {
    204: {
        'description': 'Контент отсутствует',
        'content': None
    },
    401: {
        'description': 'Пользователь неавторизован',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Не удалось подтвердить данные.'
                }
            }
        }
    }
}
