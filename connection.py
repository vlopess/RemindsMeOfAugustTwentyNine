import psycopg2

from Crypt import Crypt

class DBConnectionHandler:

    def __init__(self) -> None:
        with open('db.key', 'rb') as file:
            passwordEncoding = file.read().decode()  
            crypt = Crypt()
            password = crypt.decrypt(enc_str=passwordEncoding)     
        self.__connection_string = "host='dpg-cl32h12uuipc7385fpg0-a.oregon-postgres.render.com' dbname='victorpersonal_database' user='victorpersonal_database_user' password="+password
        self.__connection = psycopg2.connect(self.__connection_string)

    def __enter__(self):
        return self

    def getCursor(self):
        return self.__connection.cursor()
    def commitar(self):
        return self.__connection.commit()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.cursor().close()
        self.__connection.close()

