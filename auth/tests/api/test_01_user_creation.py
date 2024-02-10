import pytest
from httpx import AsyncClient

LENGTH_USERNAME = 255


async def test_01_register_user(async_client: AsyncClient) -> None:
    """Проверка регистрации пользователя."""
    response = await async_client.post('/users/jwt/register/',
                                       json={'username': 'UserTestAdmin',
                                             'email': 'usertest@test.com',
                                             'password': 'testPassword12_'})
    print(response.json())
    assert response.status_code == 201, (
        'При регистрации пользователя должен возвращаться статус-код 201.'
    )
    data = response.json()
    keys = sorted(['id', 'username', 'email', 'is_active'])
    assert sorted(list(data.keys())) == keys, (
        f'При регистрации пользователя в ответе должны быть ключи {keys}'
    )
    del data['id']
    assert data == {'username': 'UserTestAdmin',
                    'email': 'usertest@test.com',
                    'is_active': True}, (
        'При регистрации пользователя тело ответа '
        'API отличается от ожидаемого.'
    )


@pytest.mark.parametrize('json', [
    {'username': 'UserTestAdmin',
     'email': 'usertesttest.com',
     'password': 'testPassword12_'},
    {'username': 'UserTestAdmin',
     'email': 'usertest@testcom',
     'password': 'testPassword12_'},
    {'username': 'UserTestAdmin',
     'email': '@test.com',
     'password': 'testPassword12_'},
    {'username': 'UserTestAdmin',
     'email': 'u@t.c',
     'password': 'testPassword12_'},
    {'username': 'UserTestAdmin',
     'email': 'u' * 255 + '@test.com',
     'password': 'testPassword12_'}
])
async def test_02_register_invalid_email(async_client: AsyncClient,
                                         json: dict[str, str]) -> None:
    """Проверка регистрации пользователя при не валидной почты."""
    response = await async_client.post('/users/jwt/register/', json=json)
    assert response.status_code == 422, (
        'При некорректной регистрации пользователя '
        'должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной регистрации пользователя '
        'в ответе должен быть ключ `detail`.'
    )
    assert type(data['detail']) == list, (
        'При некорректной регистрации пользователя '
        'в ответе должно быть значение списком.'
    )
    error_message = (
        ('value is not a valid email address: '
         'The email address is not valid. '
         'It must have exactly one @-sign.'),
        ('value is not a valid email address: '
         'The part after the @-sign is not valid. '
         'It should have a period.'),
        ('value is not a valid email address: '
         'There must be something before the @-sign.'),
        ('Value should have at least 6 items after validation, not 5'),
        ('value is not a valid email address: '
         'The email address is too long before the @-sign '
         '(191 characters too many).')
    )
    for value in data['detail']:
        assert value['msg'] in error_message, (
            'При некорректной регистрации пользователя '
            'в ответе должно быть указано описание ошибки.'
        )


@pytest.mark.parametrize('json', [
    {'username': 'UserTestAdmin',
     'email': 'usertest@test.com',
     'password': 'testPassword12'},
    {'username': 'UserTestAdmin',
     'email': 'usertest@test.com',
     'password': 'testPassword_'},
    {'username': 'UserTestAdmin',
     'email': 'usertest@test.com',
     'password': 'testassword12_'},
    {'username': 'UserTestAdmin',
     'email': 'usertest@test.com',
     'password': 'PASSWORD12_'},
    {'username': 'UserTestAdmin',
     'email': 'usertest@test.com',
     'password': 'pass'}
])
async def test_03_invalid_password(async_client: AsyncClient,
                                   json: dict[str, str]) -> None:
    """Проверка регистрации пользователя при не валидным паролем."""
    response = await async_client.post('/users/jwt/register/', json=json)
    assert response.status_code == 422, (
        'При некорректной регистрации пользователя '
        'должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной регистрации пользователя '
        'в ответе должен быть ключ `detail`.'
    )
    assert type(data['detail']) == list, (
        'При некорректной регистрации пользователя '
        'в ответе должно быть значение списком.'
    )
    error_message = (
        ('Длина пароля меньше 8 символов.'),
        ('Пароль должен содержать: '
         'минимум одну цифру; '
         'по крайней мере один алфавит верхнего регистра; '
         'по крайней мере один алфавит нижнего регистра; '
         'по крайней мере один специальный символ, '
         'который включает в себя !#$%&()*+,-./:;<=>?@[\]^_`{|}~.')
    )
    for value in data['detail']:
        assert value['msg'] in error_message, (
            'При некорректной регистрации пользователя '
            'в ответе должно быть указано описание ошибки.'
        )


@pytest.mark.parametrize('json', [
    {'username': 'user',
     'email': 'usertest@test.com',
     'password': 'testPassword12_'},
    {'username': 'UserTestAdmin' * LENGTH_USERNAME,
     'email': 'usertest@test.com',
     'password': 'testPassword12_'}
])
async def test_04_invalid_username(async_client: AsyncClient,
                                   json: dict[str, str]) -> None:
    """Проверка регистрации пользователя при не валидным юзернейме."""
    response = await async_client.post('/users/jwt/register/',
                                       json=json)
    assert response.status_code == 422, (
        'При некорректной регистрации пользователя '
        'должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной регистрации пользователя '
        'в ответе должен быть ключ `detail`.'
    )
    assert type(data['detail']) == list, (
        'При некорректной регистрации пользователя '
        'в ответе должно быть значение списком.'
    )
    error_message = (
        ('Юзернейм меньше 6 символов.'),
        ('String should have at most 120 characters')
    )
    for value in data['detail']:
        assert value['msg'] in error_message, (
            'При некорректной регистрации пользователя '
            'в ответе должно быть указано описание ошибки.'
        )
