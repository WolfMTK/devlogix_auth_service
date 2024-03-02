RESPONSE_USER_CREATE_EXAMPLE = {
    201: {
        'description': 'Пользователь успешно создан',
        'content': {
            'application/json': {
                'example': {
                    'id': 1,
                    'username': 'UserAdmin',
                    'email': 'user@mail.com',
                    'isActive': True
                }
            }
        }
    },
    400: {
        'description': 'Ошибка запроса',
        'content': {
            'application/json': {
                'examples': {
                    'Пользователь существует (юзернейм)': {
                        'value': {
                            'detail': 'Пользователь с таким юзернеймом уже '
                                      'существует.'
                        }
                    },
                    'Пользователь существует (E-mail)': {
                        'value': {
                            'detial': 'Пользователь с такой почтой уже '
                                      'существует.'
                        }
                    },
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
                                           'The email address is too long '
                                           'before the @-sign '
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
                                           'по крайней мере один алфавит '
                                           'верхнего регистра; '
                                           'по крайней мере один алфавит '
                                           'нижнего регистра; '
                                           'по крайней мере один '
                                           'специальный символ, '
                                           'который включает в себя !#$%&('
                                           ')*+,-./:;<=>?@[\]^_`{|}~.'
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

RESPONSE_USER_GET_EXAMPLE = {
    200: {
        'description': 'Данные успешно получены',
        'content': {'application/json':
            {
                'example': {
                    'id': 1,
                    'username': 'UserAdmin',
                    'email': 'user@mail.com',
                    'isActive': True
                }
            }
        }
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

RESPONSE_USER_UPDATE_EXAMPLE = {
    200: {
        'description': 'Данные успешно обновлены',
        'content': {
            'application/json': {
                'example': {
                    'id': 1,
                    'username': 'UserAdmin',
                    'email': 'user@mail.com',
                    'firstName': 'Иван',
                    'lastName': 'Иванович',
                    'isActive': True
                }
            }
        }
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
    },
    403: {
        'description': 'Доступ запрещён',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Доступ запрещён.'
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
                                           'The email address is too long '
                                           'before the @-sign '
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
                                           'по крайней мере один алфавит '
                                           'верхнего регистра; '
                                           'по крайней мере один алфавит '
                                           'нижнего регистра; '
                                           'по крайней мере один '
                                           'специальный символ, '
                                           'который включает в себя !#$%&('
                                           ')*+,-./:;<=>?@[\]^_`{|}~.'
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
