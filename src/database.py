import psycopg2
import psycopg2.extras as extras
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

DB_HOST = os.environ.get("DB_HOST")
DB_DATABASE = os.environ.get("DB_DATABASE")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DATABASE_URL = os.environ.get("DATABASE_URL")

class Config:
    def __init__(self):
        self.config = {
            "postgres": {
                "user": DB_USER,
                "password": DB_PASSWORD,
                "host": DB_HOST,
                "database": DB_DATABASE,
                "port": 5432,
            }
        }
    
class Connection():
    def __init__(self):
        try:
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Erro na conexão", e)
            exit(1)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def copy_from(self, data, table_name):
        self.cursor.copy_from(data, table_name, sep=',')

    def insert_values(self, df, table):
        """
        Usando psycopg2.extras.execute_values() para inserir dataframe no banco de dados
        
        Params:
            conn: Connection
            df : DataFrame
            table_name: str

        Returns:
            void

        Raises: 
            DatabaseError: inserção não foi realizada com sucesso
        """

        # criando uma lista de tupples a partir dos valores do dataframe
        tuples = [tuple(x) for x in df.to_numpy()]

        # colunas de dataframe separadas por vírgula
        cols = ','.join(list(df.columns))

        # executando comando SQL para inserção
        query  = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
        
        cursor = self.cursor()
        #conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        #cur = conn.cursor()

        try:
            extras.execute_values(cursor, query, tuples)
            # self.commit()
        except (Exception, DatabaseError) as error:
            print("Error: %s" % error)
            self.rollback()
            return 1
        print("Inserção dos dados finalizada ✔")
