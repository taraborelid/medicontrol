import sqlite3

class Connectiondb():

    def __init__(self):
        self.db_file = 'ddbb/database.db'
        self.connection = None
        self.cursor = None
        self.create_connection()

    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f'Error al conectarse a la base de datos: {e}')
            self.connection = None
            self.cursor = None

    def close_connection(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()

