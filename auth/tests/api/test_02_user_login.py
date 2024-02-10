import pytest
from httpx import AsyncClient

from .constants import INVALID_LENGTH


@pytest.mark.parametrize('json', [
    {'username': 'UserTestAdmin',
     'password': 'testPassword12_'},
    {'email': 'usertest@test.com',
     'password': 'testPassword12_'}
])
async def test_01_login_user(async_client: AsyncClient,
                             json: dict[str, str]) -> None:
    """Проверка аутентификации пользователя."""
    response = await async_client.post('/users/jwt/login/',
                                       json=json)
    assert response.status_code == 200, (
        'При аутентификации пользователя должен возвращаться статус-код 200.'
    )
    data = response.json()
    keys = sorted(
        ['access_token', 'expires_in', 'refresh_token', 'token_type']
    )
    assert sorted(list(data.keys())) == keys, (
        f'При аутентификации пользователя в ответе должны быть ключи {keys}'
    )


@pytest.mark.parametrize('json', [
    {'email': 'usertesttest.com',
     'password': 'testPassword12_'},
    {'email': 'usertest@testcom',
     'password': 'testPassword12_'},
    {'email': '@test.com',
     'password': 'testPassword12_'},
    {'email': 'u@t.c',
     'password': 'testPassword12_'},
    {'email': 'usertest' * INVALID_LENGTH + '@test.com',
     'password': 'testPassword12_'}
])
async def test_02_invalid_email_login_user(
        async_client: AsyncClient,
        json: dict[str, str],
        message_email: tuple[str, ...]
) -> None:
    """Проверка аутентификации пользователя при невалидной почте."""
    response = await async_client.post('/users/jwt/login/', json=json)
    assert response.status_code == 422, (
        'При некорректной аутентификации пользователя '
        'должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной аутентификации пользователя '
        'в ответе должен быть ключ `detail`.'
    )
    assert type(data['detail']) == list, (
        'При некорректной аутентификации пользователя '
        'в ответе должно быть значение списком.'
    )
    error_message = message_email + (
        ('value is not a valid email address: '
         'Length must not exceed 2048 characters'),
    )
    for value in data['detail']:
        assert value['msg'] in error_message, (
            'При некорректной аутентификации пользователя '
            'в ответе должно быть указано описание ошибки.'
        )


@pytest.mark.parametrize('json', [
    {'username': 'UserTest',
     'password': 'testPassword12_'},
    {'username': 'UserTestAdmin',
     'password': 'test'},
    {'email': 'user@test.com',
     'password': 'testPassword12_'},
    {'email': 'usertest@test.com',
     'password': 'test'},
    {'username': 'UserTestAdmin',
     'email': 'usertest@test.com',
     'password': 'testPassword12_'},
    {'password': 'testPassword12_'},
])
async def test_03_invalid_data_login_user(
        async_client: AsyncClient,
        json: dict[str, str],
) -> None:
    """Проверка аутентификации пользователя при невалидных данных."""
    response = await async_client.post('/users/jwt/login/', json=json)
    assert response.status_code == 400, (
        'При некорректной аутентификации пользователя '
        'должен возвращаться статус-код 400.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной аутентификации пользователя '
        'в ответе должен быть ключ `detail`.'
    )
    assert type(data['detail']) == str, (
        'При некорректной аутентификации пользователя '
        'в ответе должно быть значение строкой.'
    )
    error_message = (
        ('Пароль или логин введен неверно.'),
        ('Введите username или email.'),
        ('Отсутствует username или email.')
    )
    assert data['detail'] in error_message, (
        'При некорректной аутентификации пользователя '
        'в ответе должно быть указано описание ошибки.'
    )
