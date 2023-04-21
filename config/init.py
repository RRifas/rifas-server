from config.database_schema import db, transaction_detail, rifa, transaction, users

def create_tables():
    with db:
        db.drop_tables([transaction_detail, rifa, transaction, users])
        if not db.table_exists([transaction_detail, rifa, transaction, users]):
            db.create_tables([transaction_detail, rifa, transaction, users])
            rifa.insert_many([
                {'id': 3, 'name': 'perrarina', 'goal': 100,
                    'price': 1, 'imagen': 'imagen.jpg', 'description': 'purina'},
                {'id': 1, 'name': 'carro', 'goal': 500, 'price': 20,
                    'imagen': 'asadae.jpg', 'description': 'carro blanco'},
                {'id': 2, 'name': 'libro', 'goal': 500, 'price': 100,
                    'imagen': 'imagen.jpg', 'description': 'principito'}
            ]).execute()
            users.insert_many([
                {"user_id": 1, "email": "user1@example.com", "first_name": "Ivan",
                    "last_name": "Salazar", "phone": "1234567890", "address": "123 Main St", "gender": "M"},
                {"user_id": 2, "email": "user2@example.com", "first_name": "Jane",
                    "last_name": "Doe", "phone": "0987654321", "address": "456 Oak St", "gender": "F"}
            ]).execute()
            transaction.insert_many([
                {"user_id": 2, "type_transaction": "buy", "tickets": 2},
                {"user_id": 1, "type_transaction": "buy", "tickets": 1}
            ]).execute()
            transaction_detail.insert_many([
                {'transaction_id': 1, 'rifa_id': 2, 'total': 200},
                {'transaction_id': 2, 'rifa_id': 2, 'total': 100},
            ]).execute()
