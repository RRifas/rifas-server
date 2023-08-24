import json
import pytest
from fastapi.testclient import TestClient
from model.users_connection import userConnection
from main import app


client = TestClient(app)

user_conn = userConnection()

def test_read_all():


    # Test successful read from database all rifas
    response = client.get('/')
    rifa_list = json.loads(response.content)
    result = user_conn.read_all()
    new_dict_list = [dict(
        zip(['id', 'name', 'description', 'price', 'goal', 'tickets_sold'], t)) for t in result]

    print(rifa_list, new_dict_list)
    for i in range(len(rifa_list)):
        print(i, )
        assert rifa_list[i]['id'] == new_dict_list[i]['id']
        assert rifa_list[i]['name'] == new_dict_list[i]['name']
        assert rifa_list[i]['description'] == new_dict_list[i]['description']
        assert rifa_list[i]['price'] == new_dict_list[i]['price']
        assert rifa_list[i]['goal'] == new_dict_list[i]['goal']
    assert response.status_code == 200


def test_create_a_rifa():
    test_create_a_rifa_missing_fields()


    # Test successful creation of a rifa
    rifa_data = {
        "name": "Test Rifa",
        "goal": 500,
        "price": 100,
        "imagen": "test.png",
        "description": "This is a test rifa",
    }

    response = client.post('/api/create', json=rifa_data)

    assert response.status_code == 201

    rifa_id = response.json()['id']
    user_conn.delete_rifa({'id': rifa_id})


def test_delete_rifa():


    # Test successful deletion of a rifa
    rifa_data = {
        "name": "Test Rifa",
        "goal": 100,
        "price": 100,
        "imagen": "test.png",
        "description": "This is a test rifa",
    }
    created_rifa_id = user_conn.create_a_rifa(rifa_data)

    user_conn.delete_rifa({'id': created_rifa_id[0]})

    # Check that the rifa was successfully deleted
    assert user_conn.get_rifa_by_id(created_rifa_id) is None

    # Test deletion of a non-existent rifa
    non_existent_rifa_id = 12345
    response = client.delete(f'/api/delete/{non_existent_rifa_id}')
    assert response.status_code == 404


def test_modify_rifa():


    # Test successful modification of a rifa
    rifa_data = {
        "name": "Test Rifa",
        "goal": 10000,
        "price": 100,
        "imagen": "test.png",
        "description": "This is a test rifa",
    }
    result = user_conn.create_a_rifa(rifa_data)
    assert result is not None
    assert result[1]==rifa_data['name']

    rifa_id = result[0]


    new_rifa_data = {
        "id": rifa_id,
        "name": "Test Rifa Modified",
        "goal": 5000,
        "price": 50,
        "description": "This is a modified test rifa",
    }

    result2 = user_conn.modify_rifa(new_rifa_data)

    assert result2 is not None

    # Datos inválidos para modificar la rifa
    invalid_rifa_data = {
        "id": rifa_id,
        "nombre": "Rifa de prueba modificada",
        "descripcion": "Descripción de la rifa de prueba modificada",
        "precio": "invalid_price",
        "premio": "Premio de la rifa de prueba modificada",
        "fecha_limite": "2022-01-01"
    }

    invalid_rifa_data_id = {
        "id": 999,
        "name": "Rifa de prueba modificada",
        "goal": 500,
        "price": 3,
        "imagen": "iiidjf",
        "descripcion": "2022-01-01"
    }

    # Modificar la rifa con los datos inválidos y verificar que la respuesta = status 422
    response = client.put(f'/api/update/{rifa_id}', json=invalid_rifa_data)
    assert response.status_code == 422

    # Modificar la rifa con ID inválidos y verificar que la respuesta = status 422
    response = client.put(f'/api/update/{rifa_id}', json=invalid_rifa_data_id)
    assert response.status_code == 422

    # borrar la rifa creada y modificada
    user_conn.delete_rifa({'id': rifa_id})

    # Test modification of a non-existent rifa
    with pytest.raises(Exception):
        result3 = user_conn.modify_rifa(
            {"id": 999, "name": "Test Rifa Modified"})
        rifa_id3 = result3[0]
        user_conn.delete_rifa({'id': rifa_id3})


def test_get_rifa_by_id():


    # Test successful retrieval of a rifa
    rifa_data = {
        "name": "Test Rifa",
        "goal": 10000,
        "price": 100,
        "imagen": "test.png",
        "description": "This is a test rifa",
    }
    result = user_conn.create_a_rifa(rifa_data)
    assert result is not None
    rifa_id = result[0]
    rifa_id = {'id': rifa_id}

    retrieved_rifa = user_conn.get_rifa_by_id(rifa_id)
    assert retrieved_rifa is not None
    assert retrieved_rifa["id"] == rifa_id["id"]
    user_conn.delete_rifa({'id': rifa_id['id']})

    # Test retrieval of a non-existent rifa
    retrieved_rifa = user_conn.get_rifa_by_id({'id': 999})
    assert retrieved_rifa is None


def test_create_a_rifa_missing_fields():

    # Test missing required fields
    rifa_data = {
        "goal": 500,
        "price": 100,
        "imagen": "test.png",
        "description": "This is a test rifa",
    }
    response = client.post('/api/create', json=rifa_data)
    assert response.status_code == 422

    # Test missing non-required fields
    rifa_data = {
        "name": "Test Rifa",
        "goal": 500,
        "description": "This is a test rifa",
    }
    response = client.post('/api/create', json=rifa_data)
    assert response.status_code == 422

    # Test invalid fields
    rifa_data = {
        "name": "",
        "goal": 0,
        "price": -100,
        "imagen": "test.png",
        "description": "This is a test rifa",
    }
    response = client.post('/api/create', json=rifa_data)
    assert response.status_code == 422

def test_get_ticket_price():
    rifa_id = 1
    num_tickets = 5
    expected_output = {'tickets': 5, 'total_price': 100}

    assert user_conn.get_ticket_price(rifa_id, num_tickets) == expected_output

def test_get_available_tickets():
    buy_data = {'id': 1, 'tickets': 1000}
    expected_output = {'tickets': 1000, 'total_price': 20000}

    assert user_conn.get_available_tickets(buy_data) == expected_output

def test_create_transaction():
    buy_data = {'id': 1, 'tickets': 2, 'total_price': 20}


    assert isinstance(user_conn.create_transaction(buy_data), int)

