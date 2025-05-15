import mysql.connector
from mysql.connector import Error
from config.database_config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        
    def create_connection(self):
        """Cria conexão com o MySQL"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None
            
    def close_connection(self):
        """Fecha a conexão com o banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()