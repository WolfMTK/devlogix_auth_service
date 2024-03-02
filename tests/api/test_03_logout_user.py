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
    """Проверка удаления токенов."""
    response = await async_client.post('/auth/token/login/',
                                       json=json)
    assert response.status_code == 200, (
        'При получении токенов должен возвращаться статус-код 200.'
    )
    data = response.json()
    access_token = data['accessToken']
    response = await async_client.post(
        '/auth/token/logout/',
        headers={'authorization': 'Bearer ' + access_token}
    )
    assert response.status_code == 204, (
        'При удалении токенов должен возвращаться статус-код 204.'
    )
    response = await async_client.post(
        '/auth/token/logout/',
        headers={'authorization': 'Bearer ' + access_token}
    )
    assert response.status_code == 401, (
        'При удалении токенов должен возвращаться статус-код 401.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'При повтором удалении токенов '
        'в ответе должен быть ключ `detail`.'
    )
    assert data['detail'] == 'Не удалось подтвердить данные.', (
        'При повторном удалении токенов тело ответа API отличается '
        'от ожидаемого.'
    )
