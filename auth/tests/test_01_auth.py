import pytest
from httpx import AsyncClient


async def test_01_register_user(async_client: AsyncClient) -> None:
    """Проверка регистрации пользователя."""
    response = await async_client.post('/auth/jwt/register/',
                                       json={'username': 'UserTestAdmin',
                                             'email': 'usertest@test.com',
                                             'password': 'testPassword12_'})
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
])
async def test_02_register_invalid_email(async_client: AsyncClient,
                                         json: dict[str, str]) -> None:
    """Проверка регистрации пользователя при не валидной почты."""
    response = await async_client.post('/auth/jwt/register/', json=json)
    assert response.status_code == 422, (
        'При некорректной регистрации пользователя '
        'должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной регистрации пользователя '
        'в ответе должен быть ключ `detail`.'
    )


@pytest.mark.parametrize('json', [
    {'username': 'UserTestAdmin',
     'email': 'usertest@test.com',
     'password': 'testassword12_'},
    {'username': 'UserTestAdmin',
     'email': 'usertest@testcom',
     'password': 'testPassword12'},
    {'username': 'UserTestAdmin',
     'email': 'usertest@testcom',
     'password': 'testPassword_'},
    {'username': 'UserTestAdmin',
     'email': 'usertest@testcom',
     'password': 'test'},
])
async def test_03_invalid_password(async_client: AsyncClient,
                                   json: dict[str, str]) -> None:
    """Проверка регистрации пользователя при не валидным паролем."""
    response = await async_client.post('/auth/jwt/register/', json=json)
    assert response.status_code == 422, (
        'При некорректной регистрации пользователя '
        'должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной регистрации пользователя '
        'в ответе должен быть ключ `detail`.'
    )


async def test_04_invalid_username(async_client: AsyncClient):
    """Проверка регистрации пользователя при не валидным юзернейме."""
    response = await async_client.post('/auth/jwt/register/',
                                       json={'username': 'user',
                                             'email': 'usertest@test.com',
                                             'password': 'testPassword12_'})
    assert response.status_code == 422, (
        'При некорректной регистрации пользователя '
        'должен возвращаться статус-код 422.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной регистрации пользователя '
        'в ответе должен быть ключ `detail`.'
    )


@pytest.mark.parametrize('json', [
    {'username': 'UserTestAdmin',
     'password': 'testPassword12_'},
    {'email': 'usertest@test.com',
     'password': 'testPassword12_'}
])
async def test_05_auth_user(async_client: AsyncClient,
                            json: dict[str, str]) -> None:
    """Проверка аутентификации пользователя."""
    response = await async_client.post('/auth/jwt/login/',
                                       json=json)
    assert response.status_code == 200, (
        'При аутентификации пользователя должен возвращаться статус-код 200.'
    )
    data = response.json()
    keys = sorted(
        ['access_token', 'expires_in', 'refresh_token', 'token_type']
    )
    assert sorted(list(data.keys())) == keys, (
        f'При регистрации пользователя в ответе должны быть ключи {keys}'
    )


@pytest.mark.parametrize('json', [
    {'username': 'UserTestAdmin',
     'email': 'usertest@test.com',
     'password': 'testPassword12_'},
    {'username': 'UserTest',
     'password': 'testPassword12_'},
    {'username': 'UserTestAdmin',
     'password': 'testPassword'},
    {'email': 'usertesttest.com',
     'password': 'testPassword12_'},
    {'email': 'usertest@test.com',
     'password': 'testPassword'},

])
async def test_05_auth_invalid_data(async_client: AsyncClient,
                                    json: dict[str, str]) -> None:
    """Проверка аутентификации при не валидных данных."""
    response = await async_client.post('/auth/jwt/login/', json=json)
    assert response.status_code in (422, 401), (
        'При некорректной регистрации пользователя '
        'должен возвращаться статус-код 422 или 401.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При некорректной аутентификации пользователя '
        'в ответе должен быть ключ `detail`.'
    )


@pytest.mark.parametrize('json', [
    {'username': 'UserTestAdmin',
     'password': 'testPassword12_'},
    {'email': 'usertest@test.com',
     'password': 'testPassword12_'}
])
async def test_06_logout_user(async_client: AsyncClient,
                              json: dict[str, str]) -> None:
    """Проверка очистки данных при выходе пользователя."""
    response = await async_client.post('/auth/jwt/login/',
                                       json=json)
    assert response.status_code == 200, (
        'При аутентификации пользователя должен возвращаться статус-код 200.'
    )
    data = response.json()
    access_token = data['access_token']
    response = await async_client.post(
        '/auth/jwt/logout/',
        headers={'authorization': 'Bearer ' + access_token}
    )
    assert response.status_code == 204, (
        'При выходе пользователя должен возвращаться статус-код 204.'
    )
    response = await async_client.post(
        '/auth/jwt/logout/',
        headers={'authorization': 'Bearer ' + access_token}
    )
    assert response.status_code == 401, (
        'При повтором выходе пользователя должен возвращаться статус-код 401.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При повтором выходе пользователя '
        'в ответе должен быть ключ `detail`.'
    )
    assert data['detail'] == 'Could not validate credentials', (
        'При повтором выходе пользователя тело ответа API отличается '
        'от ожидаемого.'
    )
