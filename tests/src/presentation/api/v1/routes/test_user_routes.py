from fastapi import status

from src.core.constants.permissions import UserPermissions
from tests.factories.customer_factory import CustomerFactory
from tests.factories.user_factory import UserFactory


def test_get_user_by_name_return_success(client):
    user = UserFactory()
    response = client.get(f'/api/v1/users/{user.name}/name', permissions=[UserPermissions.CAN_VIEW_USERS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == user.id
    assert data['name'] == user.name


def test_get_user_by_id_return_success(client):
    user = UserFactory()
    response = client.get(f'/api/v1/users/{user.id}/id', permissions=[UserPermissions.CAN_VIEW_USERS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == user.id
    assert data['name'] == user.name


def test_get_all_users_return_success(client):
    user1 = UserFactory()
    user2 = UserFactory()

    response = client.get('/api/v1/users', permissions=[UserPermissions.CAN_VIEW_USERS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {'id': user1.id, 'name': user1.name},
        {'id': user2.id, 'name': user2.name}
    ]


def test_update_user_return_success(client):
    customer = CustomerFactory(user__password='oldpass123')
    payload = {'old_password': 'oldpass123', 'password': 'new_pass'}

    response = client.put('/api/v1/users/change-password', json=payload, permissions=[UserPermissions.CAN_UPDATE_USER])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        'message': 'Password updated successfully',
        'status': 'success',
    }
