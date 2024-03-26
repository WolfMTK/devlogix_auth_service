RESPONSE_LOGOUT_EXAMPLE = {
    204: {
        'description': 'Successful Response',
        'content': None
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
