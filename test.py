if __name__ == '__main__':
    import jwt
    print(jwt.encode({'sub': 'UserAdmin'}, 'token', algorithm='HS256'))