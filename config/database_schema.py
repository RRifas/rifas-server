
import datetime
import psycopg2
from peewee import *


db = PostgresqlDatabase('rifas', host='localhost', port=5432, user='postgres', password='pass')

class Basemodel(Model):
    
    class Meta:
        database=db
        


class users(Basemodel):
    user_id=AutoField()
    email=CharField(unique=True, index=True)
    first_name=CharField(null=True)
    last_name=CharField(null=True)
    phone=IntegerField(unique=True)
    create_at=DateTimeField(default=datetime.datetime.now)
    address=CharField(null=True)
    gender=CharField(null=True)
    

    
class transaction(Basemodel):
    transaction_id=AutoField()
    user_id=ForeignKeyField(users,backref='transactions')
    type_transaction=CharField(null=True)
    tickets=IntegerField()
    transaction_date=DateTimeField(default=datetime.datetime.now)
    

class rifa(Basemodel):
    rifa_id=AutoField()
    rifa_name=CharField(null=True)
    goal=IntegerField()
    price=IntegerField()

class transaction_detail(Basemodel):
    transaction_detail_id=AutoField()
    transaction_id=ForeignKeyField(transaction,backref='transactions_details')
    rifa_id=ForeignKeyField(rifa,backref='transactions_details')
    total=IntegerField()
    
    
if __name__=='__main__':
    if not db.table_exists([transaction_detail,rifa,transaction,users]):
        db.create_tables([transaction_detail,rifa,transaction,users])
    
    
