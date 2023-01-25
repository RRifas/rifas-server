from sqlite3 import OperationalError
import psycopg
from datetime import datetime






class userConnection():
    conn=None
    def __init__(self):
        try:
            self.conn= psycopg.connect("dbname=rifas host=localhost port=5432 user=postgres password=pass")
        except psycopg.OperationalError as err:
            print(err)
            self.conn.close()

    def read_all(self):
        aver=[]
        with self.conn.cursor() as cur:
            data =cur.execute(""" select rifa.rifa_name, rifa.goal,rifa.rifa_id, SUM(transaction_detail.tickets) from transaction_detail LEFT JOIN rifa ON rifa.rifa_id = transaction_detail.rifa_id GROUP BY rifa.rifa_id;
""")
            data=data.fetchall()
            
            if not data:
                with self.conn.cursor() as cur:
                     data=cur.execute(""" select rifa_name,goal,rifa_id from rifa;""")

                     data=data.fetchall()
               
               
            print(data)
            
            
            

            

            


            

            return data

    def preorder_a_ticket(self,data):
        with self.conn.cursor() as cur:
            
            # rifa_id=data['rifa_id']
            
            #rifa_id=str(rifa_id)
            
            #price=cur.execute("SELECT price from rifa WHERE rifa_id=%(rifa_id)s",{"rifa_id": rifa_id})
            
            #price= price.fetchone()[0]
            
            #amount=price*data['tickets']

            #data['amount']=amount

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            data['transaction_date']=dt_string 


            cur.execute(""" 
            INSERT INTO transaction(user_id,tickets,transaction_date) VALUES(2,%(tickets)s,%(transaction_date)s)""",data)
            
        self.conn.commit()
                
    def buy_a_ticket(self,data):
        with self.conn.cursor() as cur:


            rifa_id=data['rifa_id']
            
            rifa_id=str(rifa_id)
            
            price=cur.execute("SELECT price from rifa WHERE rifa_id=%(rifa_id)s",{"rifa_id": rifa_id})
            
            price= price.fetchone()[0]
            
            total=price*data['tickets']

            data['total']=total

            cur.execute("""
            INSERT INTO transaction_detail(transaction_id,rifa_id,total) VALUES(%(transaction_id)s,%(rifa_id)s,%(total)s)""",data)
        self.conn.commit()

    def cancel_ticket(self,id):
        with self.conn.cursor() as cur:
             cur.execute("DELETE FROM transaction WHERE transaction_id=%(transaction_id)s",{"transaction_id": id})
            
        self.conn.commit()

    def create_a_rifa(self,data):
        with self.conn.cursor() as cur:
            
            cur.execute(""" 
            INSERT INTO rifa(rifa_name,goal,price) VALUES(%(rifa_name)s,%(goal)s,%(price)s)""",data)

        self.conn.commit()

    def delete_rifa(self,id):
        with self.conn.cursor() as cur:
             cur.execute("DELETE FROM rifa WHERE rifa_id=%(rifa_id)s",{"rifa_id": id})
            
        self.conn.commit()

    def modify_rifa(self,id):
        with self.conn.cursor() as cur:
            cur.execute(""" update "rifa" SET rifa_name = %(rifa_name)s, goal=%(goal)s, price=%(price)s Where rifa_id = %(rifa_id)s""",id)

        self.conn.commit()

    
    def __def__(self):
        self.conn.close()




