RESPONSE_USER_GET_EXAMPLE = {
    200: {
        'description': 'Successful Response',
        'content': {'application/json':
            {
                'example': {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                    'username': 'UserAdmin',
                    'email': 'user@mail.com',
                }
            }
        }
    },
    401: {
        'description': 'Unauthorized',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Invalid authentication credentials.'
                }
            }
        }
    }
}
