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
                    rifa.id, rifa.name, rifa.description, rifa.price, rifa.goal, SUM(transaction.tickets) as total_tickets
                    FROM transaction_detail
                    FULL JOIN rifa on rifa.id = transaction_detail.rifa_id
                    FULL JOIN transaction on transaction_detail.transaction_id = transaction.transaction_id
                    GROUP BY rifa.id
        """

                    cur.execute(query)
                    self.data = cur.fetchall()
                    return self.data
            except psycopg.Error as e:
                logger.error(f"Error al seleccionar las rifas: {e}")
                raise e

    # Create a new Rifa in database
    def create_a_rifa(self, data):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    query = """
    INSERT INTO rifa(name, goal, price, imagen, description)
    VALUES(%(name)s::text, %(goal)s::numeric, %(price)s::numeric, %(imagen)s::text, %(description)s::text)
    RETURNING id, name"""

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
                    query = """DELETE FROM rifa WHERE id=%(id)s"""
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
                    SET name = %(name)s, goal=%(goal)s, price=%(price)s, description=%(description)s
                    WHERE id = %(id)s RETURNING id, name, description"""
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
                    query = """SELECT id FROM rifa WHERE id = %(id)s"""
                    cur.execute(query, id)
                    result = cur.fetchone()
                    if not result:
                        print("HERE")
                        return None
                    return {
                        "id": result[0],
                    }
            except psycopg.Error as e:
                logger.error("Error fetching rifa by id:", e)
                raise e


    def get_ticket_price(self, id, num_tickets):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    query = """SELECT price FROM rifa WHERE id = %(id)s"""
                    cur.execute(query, {'id': id})
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
                            FULL JOIN rifa on rifa.id = transaction_detail.rifa_id
                            FULL JOIN transaction on transaction_detail.transaction_id = transaction.transaction_id
                            WHERE rifa.id=%(id)s
                            GROUP BY rifa.id"""

                    cur.execute(query, {'id': buy_data['id']})
                    result = cur.fetchone()

                    if result[1] is None:
                        return self.get_ticket_price(buy_data['id'], buy_data['tickets'])

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
            data = cur.execute(' select name,id from rifa where;')

            data = data.fetchall()

            return data

    def __def__(self):
        self.conn.close()



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

