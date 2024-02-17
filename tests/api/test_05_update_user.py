import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('json', [
    {'login': {'username': 'UserTestAdmin',
               'password': 'testPassword12_'},
     'data': {'first_name': 'Иван',
              'email': 'usertest@test.com',
              'last_name': 'Иванович',
              'username': 'UserTestAdmin2',
              'password': 'testPassword12_2'}},
    {'login': {'email': 'usertest@test.com',
               'password': 'testPassword12_'},
     'data': {'first_name': 'Иван',
              'last_name': 'Иванович',
              'email': 'usertest2@test.com',
              'username': 'UserTestAdmin',
              'password': 'testPassword12_2'}}
])
async def test_01_update_user(async_client: AsyncClient,
                              json: dict[str, str]) -> None:
    """Проверка обновления данных пользователя."""
    response = await async_client.post('/auth/token/login/',
                                       json=json['login'])
    assert response.status_code == 200, (
        'При получении токенов должен возвращаться статус-код 200.'
    )
    data = response.json()
    access_token = data['access_token']
    response = await async_client.patch(
        '/users/me/',
        headers={'authorization': 'Bearer ' + access_token},
        json=json['data']
    )
    assert response.status_code == 200, (
        'При обновлении данных должен возвращаться статус-код 200.'
    )
    data = response.json()
    password = json['data']['password']
    del json['data']['password']
    keys = sorted(list(json['data'].keys()) + ['id', 'is_active'])
    assert sorted(list(data.keys())) == keys, (
        f'При обновлении пользователя в ответе должны быть ключи {keys}'
    )
    del data['id']
    assert data == json['data'] | {'is_active': True}, (
        'При регистрации пользователя тело ответа '
        'API отличается от ожидаемого.'
    )
    email = json['data']['email']
    response = await async_client.post('/auth/token/login/',
                                       json={'email': email,
                                             'password': password})
    assert response.status_code == 200, (
        'При получении токенов должен возвращаться статус-код 200.'
    )
    data = response.json()
    access_token = data['access_token']

    if json['login'].get('username'):
        response = await async_client.patch(
            '/users/me/',
            headers={'authorization': 'Bearer ' + access_token},
            json=json['login']
        )
    else:
        response = await async_client.patch(
            '/users/me/',
            headers={'authorization': 'Bearer ' + access_token},
            json=json['login']
        )
    assert response.status_code == 200, (
        'При обновлении данных должен возвращаться статус-код 200.'
    )
