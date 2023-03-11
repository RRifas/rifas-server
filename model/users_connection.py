<<<<<<< HEAD
import psycopg
from uuid import uuid4
import datetime
import logging
from config.database_schema import database_dsn

#Create logger instance
logger = logging.getLogger(__name__)

#Database Connection class using context manager
class DatabaseConnection:
    def __init__(self):
        self.conn = None

# Connect to database when entering context
    def __enter__(self):
        try:
            self.conn = psycopg.connect(database_dsn)
            return self.conn
        except psycopg.OperationalError as err:
            logger.error(f"Error connecting to database:{err}")
            if self.conn:
                self.conn.close()
            raise ConnectionError("Error connecting to database")

# Close connection when exiting context
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
        if isinstance(exc_value, psycopg.Error):
            logger.error(f"Error executing database operation: {exc_value}")
            return False
        return True

#UserConnection class for CRUD operations on Rifa table
class userConnection():
    def __init__(self):
        self.db_conn = DatabaseConnection()

    # Read all Rifa data from database
    def read_all(self):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    query = """ SELECT
                    rifa.rifa_name, rifa.description, rifa.price, rifa.goal, SUM(transaction.tickets) as total_tickets
                    FROM transaction_detail 
                    FULL JOIN rifa on rifa.rifa_id = transaction_detail.rifa_id 
                    FULL JOIN transaction on transaction_detail.transaction_id = transaction.transaction_id
                    GROUP BY rifa.rifa_id
        """

                    cur.execute(query)
                    self.data = cur.fetchall()
                    return self.data
            except psycopg.Error as e:
                logger.error(f"Error al crear la rifa: {e}")
                raise e

    # Create a new Rifa in database
    def create_a_rifa(self, data):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    query = """ 
    INSERT INTO rifa(rifa_name, goal, price, imagen, description) 
    VALUES(%(rifa_name)s::text, %(goal)s::numeric, %(price)s::numeric, %(imagen)s::text, %(description)s::text) 
    RETURNING rifa_id, rifa_name"""

                    cur.execute(query, data)
                    self.id = cur.fetchone()
                    conn.commit()
                    return self.id
            except psycopg.Error as e:
                logger.error(f"Error creating rifa: {e}")
                raise e

    # Delete a Rifa from database
    def delete_rifa(self, id):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    query = """DELETE FROM rifa WHERE rifa_id=%(id)s"""
                    cur.execute(query, {'id': id['id']})
                    conn.commit()
            except psycopg.Error as e:
                logger.error(f"Error modifying rifa: {e}")
                raise e

    # Modify a Rifa in database
    def modify_rifa(self, id):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    query = """ UPDATE "rifa" 
                    SET rifa_name = %(rifa_name)s, goal=%(goal)s, price=%(price)s, description=%(description)s 
                    WHERE rifa_id = %(rifa_id)s RETURNING rifa_id, rifa_name, description"""
                    cur.execute(query, id)
                    self.data = cur.fetchone()

                conn.commit()
                return self.data
            except psycopg.Error as e:
                logger.error(f"Error modifying rifa: {e}")
                raise e

    # Get Rifa from database by ID
    def get_rifa_by_id(self, id):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:

                    query = """SELECT rifa_id FROM rifa WHERE rifa_id = %(id)s"""
                    cur.execute(query, id)

                    result = cur.fetchone()
                    if not result:
                        return None
                    return {
                        "rifa_id": result[0],
                    }
            except psycopg.Error as e:
                logger.error("Error fetching rifa by id:", e)
                raise e


    def get_ticket_price(self, rifa_id, num_tickets):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    query = """SELECT price FROM rifa WHERE rifa_id = %(id)s"""
                    cur.execute(query, {'id': rifa_id})
                    result = cur.fetchone()

                    if not result:
                        return None

                    ticket_price = result[0]
                    total_price = num_tickets * ticket_price
                    return {'tickets': num_tickets, 'total_price': total_price}

            except psycopg.Error as e:
                logger.error("Error fetching ticket price:", e)
                raise e


    def get_available_tickets(self, buy_data):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    query = """SELECT price, SUM(transaction.tickets) as total_tickets
                            FROM transaction_detail
                            FULL JOIN rifa on rifa.rifa_id = transaction_detail.rifa_id
                            FULL JOIN transaction on transaction_detail.transaction_id = transaction.transaction_id
                            WHERE rifa.rifa_id=%(id)s
                            GROUP BY rifa.rifa_id"""

                    cur.execute(query, {'id': buy_data['rifa_id']})
                    result = cur.fetchone()

                    if result[1] is None:
                        return self.get_ticket_price(buy_data['rifa_id'], buy_data['tickets'])

                    if result[0] is not None and result[1] <= 999:
                        ticket_price = result[0]
                        total_price = buy_data['tickets'] * ticket_price
                        return {'tickets': buy_data['tickets'], 'total_price': total_price}

                    return None

            except psycopg.Error as e:
                logger.error("Error fetching available tickets:", e)
                raise e

    def read(self):
        with self.conn.cursor() as cur:
            data = cur.execute(' select rifa_name,rifa_id from rifa where;')

            data = data.fetchall()

            return data

=======
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

    
>>>>>>> origin/main
    def __def__(self):
        self.conn.close()



<<<<<<< HEAD
    def create_transaction(self, buy_data):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    # Crear una nueva transacción
                    user_id = 1
      
                    
                    result=cur.execute(
                             "INSERT INTO transaction (user_id, type_transaction, tickets, transaction_date) VALUES (%s, %s, %s, %s) RETURNING transaction_id",
                    (user_id, 'buy', buy_data['tickets'], datetime.datetime.now())
                )
                    
                    
                    conn.commit()
                    #Crear un nuevo detalle de transacción
                    result2=cur.execute(
                        "INSERT INTO transaction_detail (transaction_id, rifa_id, total) VALUES (%s, %s, %s) RETURNING transaction_detail_id",
                        (result.fetchone()[0], buy_data['rifa_id'], buy_data['total_price']) 
                    )

                    conn.commit()

                # Devolver el id de la transacción creada
                    return result2.fetchone()[0]

            except psycopg.Error as e:
                logger.error(f"Error creating transaction: {e}")
                raise e
            
=======

>>>>>>> origin/main
