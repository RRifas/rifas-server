import psycopg
from passlib.hash import bcrypt
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

          # Get Rifa from database by ID
    def register(self, data):
        with self.db_conn as conn:
            try:
                with conn.cursor() as cur:
                    data["create_at"] = datetime.datetime.now()
                    hashed_password = bcrypt.hash(data["password"])  
                    data["password"] = hashed_password
                    query = """
    INSERT INTO users(email, first_name, last_name, phone,create_at, address,gender,password)
    VALUES(%(email)s::text, %(first_name)s::text, %(last_name)s::text,%(phone)s::numeric,%(create_at)s::timestamp,%(address)s::text,%(gender)s::text,%(password)s::text)
    RETURNING email """

                    cur.execute(query, data)
                    self.id = cur.fetchone()
                    conn.commit()
                    return self.id
            except psycopg.Error as e:
                logger.error(f"Error creating users: {e}")
                raise e  
    
    def login_auth(self,email,password):
        with self.db_conn as conn:

            try:
                with conn.cursor() as cur:
                    query = """
                    SELECT email, password FROM users WHERE email = %(email)s
                    """
                    cur.execute(query, {"email": email})
                    user = cur.fetchone()

                    if user and bcrypt.verify(password, user[1]):
                        
                        # Devolver los datos del usuario autenticado si la contraseña es correcta
                        return user[0]
                        
                    else:
                        return None  # Credenciales incorrectas

            except psycopg.Error as e:
                logger.error(f"Error retrieving user for login: {e}")
                raise e

    


    def __def__(self):
        self.conn.close()