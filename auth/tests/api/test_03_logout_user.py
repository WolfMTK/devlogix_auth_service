import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('json', [
    {'username': 'UserTestAdmin',
     'password': 'testPassword12_'},
    {'email': 'usertest@test.com',
     'password': 'testPassword12_'}
])
async def test_01_logout_user(async_client: AsyncClient,
                              json: dict[str, str]) -> None:
    """Проверка очистки данных при выходе пользователя."""
    response = await async_client.post('/users/jwt/login/',
                                       json=json)
    assert response.status_code == 200, (
        'При аутентификации пользователя должен возвращаться статус-код 200.'
    )
    data = response.json()
    access_token = data['access_token']
    response = await async_client.post(
        '/users/jwt/logout/',
        headers={'authorization': 'Bearer ' + access_token}
    )
    assert response.status_code == 204, (
        'При выходе пользователя должен возвращаться статус-код 204.'
    )
    response = await async_client.post(
        '/users/jwt/logout/',
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
    assert data['detail'] == 'Не удалось подтвердить данные.', (
        'При повтором выходе пользователя тело ответа API отличается '
        'от ожидаемого.'
    )
