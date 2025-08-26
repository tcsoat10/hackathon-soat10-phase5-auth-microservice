from fastapi import status
from src.core.constants.permissions import PersonPermissions
from tests.factories.person_factory import PersonFactory
from pycpfcnpj import gen


def test_get_person_by_cpf_and_return_success(client):
    person = PersonFactory()
    
    response = client.get(f"/api/v1/person/{person.cpf}/cpf", permissions=[PersonPermissions.CAN_VIEW_PERSONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data
    assert data["cpf"] == person.cpf
    assert data["name"] == person.name
    assert data["email"] == person.email
    

def test_get_person_by_id_and_return_success(client):
    person = PersonFactory()
    
    response = client.get(f"/api/v1/person/{person.id}/id", permissions=[PersonPermissions.CAN_VIEW_PERSONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data
    assert data["cpf"] == person.cpf
    assert data["name"] == person.name
    assert data['id'] == person.id


def test_get_all_person_return_success(client):
    person1 = PersonFactory()
    person2 = PersonFactory()
    
    response = client.get("/api/v1/person", permissions=[PersonPermissions.CAN_VIEW_PERSONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {
            "id": person1.id,
            "cpf": person1.cpf,
            "name": person1.name,
            "email": person1.email,
            "birth_date": person1.birth_date.strftime('%Y-%m-%d')
        },
        {
            "id": person2.id,
            "cpf": person2.cpf,
            "name": person2.name,
            "email": person2.email,
            "birth_date": person2.birth_date.strftime('%Y-%m-%d')
        }
    ]

def test_update_person_and_return_success(client):
    person = PersonFactory()
    
    cpf = gen.cpf()
    payload = {
        'id': person.id,
        "cpf": cpf,
        "name": "JOÃO - UPDATED",
        "email": "joao@gmail.com",
        "birth_date": "1999-01-01"
    }

    response = client.put(f"/api/v1/person/{person.id}", json=payload, permissions=[PersonPermissions.CAN_UPDATE_PERSON])

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {
        "id": person.id,
        "cpf": cpf,
        "name": "JOÃO - UPDATED",
        "email": "joao@gmail.com",
        "birth_date": "1999-01-01"
    }

def test_delete_person_and_return_success(client):
    person = PersonFactory()

    response = client.delete(f"/api/v1/person/{person.id}", permissions=[PersonPermissions.CAN_DELETE_PERSON])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/api/v1/person", permissions=[PersonPermissions.CAN_VIEW_PERSONS])
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == 0
    assert data == []