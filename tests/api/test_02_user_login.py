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
    """Проверка получения токенов."""
    response = await async_client.post('/auth/token/login/',
                                       json=json)
    assert response.status_code == 200, (
        'При получении токенов должен возвращаться статус-код 200.'
    )
    data = response.json()
    keys = sorted(
        ['accessToken', 'expiresIn', 'refreshToken', 'tokenType']
    )
    assert sorted(list(data.keys())) == keys, (
        f'При получении токенов в ответе должны быть ключи {keys}'
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
    """Проверка получения токенов при невалидной почте."""
    response = await async_client.post('/auth/token/login/', json=json)
    assert response.status_code == 422, (
        'При некорректном получении токенов '
        'должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректном получении токенов '
        'в ответе должен быть ключ `detail`.'
    )
    assert isinstance(data['detail'], list), (
        'При некорректном получении токенов '
        'в ответе должно быть значение списком.'
    )
    error_message = message_email + (
        ('value is not a valid email address: '
         'Length must not exceed 2048 characters'),
    )
    for value in data['detail']:
        assert value['msg'] in error_message, (
            'При некорректном получении токенов '
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
    """Проверка получения токенов при невалидных данных."""
    response = await async_client.post('/auth/token/login/', json=json)
    assert response.status_code == 400, (
        'При некорректном получении токенов '
        'должен возвращаться статус-код 400.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректном получении токенов '
        'в ответе должен быть ключ `detail`.'
    )
    assert type(data['detail']) == str, (
        'При некорректном получении токенов '
        'в ответе должно быть значение строкой.'
    )
    error_message = (
        ('Пароль или логин введен неверно.'),
        ('Введите username или email.'),
        ('Отсутствует username или email.')
    )
    assert data['detail'] in error_message, (
        'При некорректном получении токенов '
        'в ответе должно быть указано описание ошибки.'
    )
