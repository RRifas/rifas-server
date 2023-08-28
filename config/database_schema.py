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
    email = CharField()
    first_name = CharField(null=False, default='')
    last_name = CharField(null=False, default='')
    phone = CharField(unique=True, null=False, default='') 
    create_at = DateTimeField(default=datetime.datetime.now)
    address = CharField(null=False, default='')
    gender = CharField(null=False, default='')
    password = CharField(null=True, default='')


class transaction(Basemodel):
    transaction_id = AutoField()
    user_id = ForeignKeyField(users, backref='transactions')
    type_transaction = CharField(null=True)
    tickets = IntegerField(null=False, default='')
    transaction_date = DateTimeField(default=datetime.datetime.now)


class rifa(Basemodel):
    id = AutoField(null=False, default='')
    name = CharField(null=False, default='')
    goal = IntegerField(null=False, default='')
    price = IntegerField(null=False, default='')
    imagen = CharField(null=False, default='')
    description = CharField(null=False, default='')


class transaction_detail(Basemodel):
    transaction_detail_id = AutoField()
    transaction_id = ForeignKeyField(
        transaction, backref='transactions_details')
    rifa_id = ForeignKeyField(rifa, backref='transactions_details', on_delete='CASCADE')
    total = IntegerField(null=False, default='')
