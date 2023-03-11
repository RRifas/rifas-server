import datetime
from peewee import PostgresqlDatabase, Model, CharField, DateTimeField, AutoField, IntegerField, ForeignKeyField
from config.config import db_name, db_password, db_host, db_port, db_user

database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

database_dsn = f"host={db_host} dbname={db_name} user={db_user} password={db_password} port={db_port}"

db = PostgresqlDatabase(database_url)


class Basemodel(Model):
    class Meta:
        database = db


class users(Basemodel):
    user_id = AutoField()
    email = CharField(unique=True, index=True)
    first_name = CharField(null=False, default='')
    last_name = CharField(null=False, default='')
    phone = IntegerField(unique=True, null=False, default='')
    create_at = DateTimeField(default=datetime.datetime.now)
    address = CharField(null=False, default='')
    gender = CharField(null=False, default='')


class transaction(Basemodel):
    transaction_id = AutoField()
    user_id = ForeignKeyField(users, backref='transactions')
    type_transaction = CharField(null=True)
    tickets = IntegerField(null=False, default='')
    transaction_date = DateTimeField(default=datetime.datetime.now)


class rifa(Basemodel):
    rifa_id = AutoField(null=False, default='')
    rifa_name = CharField(null=False, default='')
    goal = IntegerField(null=False, default='')
    price = IntegerField(null=False, default='')
    imagen = CharField(null=False, default='')
    description = CharField(null=False, default='')


class transaction_detail(Basemodel):
    transaction_detail_id = AutoField()
    transaction_id = ForeignKeyField(
        transaction, backref='transactions_details')
    rifa_id = ForeignKeyField(rifa, backref='transactions_details')
    total = IntegerField(null=False, default='')


if __name__ == '__main__':
    if not db.table_exists([transaction_detail, rifa, transaction, users]):
        db.create_tables([transaction_detail, rifa, transaction, users])
        rifa.insert_many([
            {'rifa_id': 3, 'rifa_name': 'perrarina', 'goal': 100,
                'price': 1, 'imagen': 'imagen.jpg', 'description': 'purina'},
            {'rifa_id': 1, 'rifa_name': 'carro', 'goal': 500, 'price': 20,
                'imagen': 'asadae.jpg', 'description': 'carro blanco'},
            {'rifa_id': 2, 'rifa_name': 'libro', 'goal': 500, 'price': 100,
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
