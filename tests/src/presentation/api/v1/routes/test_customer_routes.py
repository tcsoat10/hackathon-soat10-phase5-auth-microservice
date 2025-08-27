from tests.factories.customer_factory import CustomerFactory
from src.core.exceptions.utils import ErrorCode
from src.core.constants.permissions import CustomerPermissions
from pycpfcnpj import gen

from fastapi import status
from datetime import datetime

from tests.factories.profile_factory import ProfileFactory

def test_create_customer_success(client):
    ProfileFactory(name="customer")
    payload = {
        'person': {
            'name': 'John Doe',
            'cpf': '28506767563',
            'email': 'jonhdoe@example.com',
            'birth_date': '1990-01-01'
        },
        "user": {
            "name": "john.doe",
            "password": "12345678",
            
        }
    }

    response = client.post('/api/v1/customers', json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    assert response.json() == {
        'id': 1,
        'person': {
            'id': 1,
            'birth_date': '1990-01-01',
            'cpf': '28506767563',
            'email': 'jonhdoe@example.com',
            'name': 'John Doe',
        },
    }

def test_create_customer_with_existing_cpf_return_error(client):
    existing_customer = CustomerFactory(user__profile__name='customer')
    payload = {
        'person': {
            'name': 'Different Name',
            'cpf': existing_customer.person.cpf,
            'email': 'different@example.com',
            'birth_date': '1995-02-02'
        },
        "user": {
            "name": "existing.user",
            "password": "12345678"
        }
    }

    response = client.post('/api/v1/customers', json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Customer already exists.',
            'details': None,
        }
    }

def test_create_customer_with_existing_email_return_error(client):
    existing_customer = CustomerFactory(user__profile__name='customer')
    payload = {
        'person': {
            'name': 'Different Name',
            'cpf': gen.cpf(),
            'email': existing_customer.person.email,
            'birth_date': '1995-02-02'
        },
        "user": {
            "name": "user.name",
            "password": "12345678"
        }
    }

    response = client.post('/api/v1/customers', json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Customer already exists.',
            'details': None,
        }
    }

def test_create_inactive_customer_success(client):
    inactive_customer = CustomerFactory(
        user__profile__name='customer',
        inactivated_at=datetime.now(),
    )
    payload = {
        'person': {
            'name': 'New Name',
            'cpf': inactive_customer.person.cpf,
            'email': 'newemail@example.com',
            'birth_date': '1995-02-02'
        },
        "user": {
            "name": "user.name",
            "password": "12345678"
        }
    }

    response = client.post('/api/v1/customers', json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['person']['cpf'] == inactive_customer.person.cpf
    assert data['person']['email'] == payload['person']['email']

def test_update_inactive_customer_return_error(client):
    inactive_customer = CustomerFactory(inactivated_at=datetime.now())
    payload = {
        'id': inactive_customer.id,
        'person': {
            'id': inactive_customer.person.id,
            'cpf': inactive_customer.person.cpf,
            'name': 'New Name',
            'email': 'newemail@example.com',
            'birth_date': '1995-02-02'
        }
    }

    response = client.put(f'/api/v1/customers/{inactive_customer.id}', json=payload, permissions=[CustomerPermissions.CAN_UPDATE_CUSTOMER])
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Customer not found.',
            'details': None,
        }
    }




def test_create_duplicate_customer_return_error(client):
    customer = CustomerFactory(user__profile__name='customer')
    payload = {
        'person': {
            'name': customer.person.name,
            'cpf': customer.person.cpf,
            'email': customer.person.email,
            'birth_date': customer.person.birth_date.strftime('%Y-%m-%d')
        },
        "user": {
            "name": "user.name",
            "password": "12345678"
        }
    }

    response = client.post('/api/v1/customers', json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Customer already exists.',
            'details': None,
        }
    }


def test_reactivate_customer_return_success(client):
    customer = CustomerFactory(
        user__profile__name='customer',
        inactivated_at=datetime.now(),
    )
    payload = {
        'person': {
            'name': customer.person.name,
            'cpf': customer.person.cpf,
            'email': customer.person.email,
            'birth_date': customer.person.birth_date.strftime('%Y-%m-%d')
        },
        "user": {
            "name": "user.name",
            "password": "12345678"
        }
    }

    response = client.post('/api/v1/customers', json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['person']['id'] == customer.person_id


def test_get_customer_by_id_success(client):
    customer = CustomerFactory()

    response = client.get(f'/api/v1/customers/{customer.id}/id', permissions=[CustomerPermissions.CAN_VIEW_CUSTOMERS])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert 'id' in data
    assert data['id'] == customer.id
    assert data['person']['id'] == customer.person_id

def test_get_customer_by_person_id_success(client):
    customer = CustomerFactory()

    response = client.get(f'/api/v1/customers/{customer.person_id}/person_id', permissions=[CustomerPermissions.CAN_VIEW_CUSTOMERS])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert 'id' in data
    assert data['id'] == customer.id
    assert data['person']['id'] == customer.person_id


def test_get_all_customers_success(client):
    customer1 = CustomerFactory()
    customer2 = CustomerFactory()

    response = client.get('/api/v1/customers', permissions=[CustomerPermissions.CAN_VIEW_CUSTOMERS])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {
            'id': customer1.id,
            'person': {
                'id': customer1.person.id,
                'name': customer1.person.name,
                'cpf': customer1.person.cpf,
                'email': customer1.person.email,
                'birth_date': customer1.person.birth_date.strftime('%Y-%m-%d')
            }
            
        },
        {
            'id': customer2.id,
            'person': {
                'id': customer2.person.id,
                'name': customer2.person.name,
                'cpf': customer2.person.cpf,
                'email': customer2.person.email,
                'birth_date': customer2.person.birth_date.strftime('%Y-%m-%d')
            }
            
        }
    ]


def test_update_customer_success(client):
    customer = CustomerFactory()

    payload = {
        'id': customer.id,
        'person': {
            'id': customer.person.id,
            'cpf': customer.person.cpf,
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'birth_date': '1990-01-01'
        }
    }

    response = client.put(f'/api/v1/customers/{customer.id}', json=payload, permissions=[CustomerPermissions.CAN_UPDATE_CUSTOMER])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        'id': customer.id,
        'person': {
            'id': customer.person.id,
            'cpf': customer.person.cpf,
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'birth_date': '1990-01-01'
        }
    }


def test_delete_customer_success(client):
    customer1 = CustomerFactory()
    customer2 = CustomerFactory()

    response = client.delete(f'/api/v1/customers/{customer1.id}', permissions=[CustomerPermissions.CAN_DELETE_CUSTOMER])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/v1/customers', permissions=[CustomerPermissions.CAN_VIEW_CUSTOMERS])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [{
        'id': customer2.id,
            'person': {
                'id': customer2.person.id,
                'name': customer2.person.name,
                'cpf': customer2.person.cpf,
                'email': customer2.person.email,
                'birth_date': customer2.person.birth_date.strftime('%Y-%m-%d')
            }
    }]