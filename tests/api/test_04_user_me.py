import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('json', [
    {
        'login': {'username': 'UserTestAdmin',
                  'password': 'testPassword12_'},
        'data': {
            'username': 'UserTestAdmin',
            'email': 'usertest@test.com',
            'isActive': True
        }
    },
    {
        'login': {'email': 'usertest@test.com',
                  'password': 'testPassword12_'},
        'data': {
            'username': 'UserTestAdmin',
            'email': 'usertest@test.com',
            'isActive': True
        }
    }
])
async def test_01_user_me(async_client: AsyncClient,
                          json: dict[str, dict[str, str]]) -> None:
    """Проверка получения данных о себе."""
    response = await async_client.post('/auth/token/login/',
                                       json=json['login'])
    assert response.status_code == 200, (
        'При получении токенов должен возвращаться статус-код 200.'
    )
    data = response.json()
    access_token = data['accessToken']
    response = await async_client.get(
        '/users/me/',
        headers={'authorization': 'Bearer ' + access_token}
    )
    assert response.status_code == 200, (
        'При получении данных о себе должен возвращаться статус-код 204.'
    )
    data = response.json()
    keys = sorted(list(json['data']) + ['id'])
    assert sorted(list(data.keys())) == keys, (
        f'При получении данных о себе в ответе должны быть ключи {keys}'
    )
    del data['id']
    assert data == json['data'], (
        'При получении данных о себе тело ответа '
        'API отличается от ожидаемого.'
    )


async def test_02_invalid_user_me(async_client: AsyncClient):
    """Проверка данных о себе при невалидных данных."""
    response = await async_client.get('/users/me/',)
    assert response.status_code == 401, (
        'При получении данных о себе должен возвращаться статус-код 204.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При получении данных о себе '
        'в ответе должен быть ключ `detail`.'
    )
    assert data['detail'] == 'Не удалось подтвердить данные.', (
        'При получении данных о себе тело ответа API отличается '
        'от ожидаемого.'
    )
