import psycopg2 as db
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

DB_HOST = os.environ.get("DB_HOST")
DB_DATABASE = os.environ.get("DB_DATABASE")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

connection = db.connect(dbname=DB_DATABASE, host=DB_HOST, user=DB_USER, password=DB_PASSWORD)

cursor = connection.cursor()

# cursor.execute("SELECT * FROM cenario1_salas")

# print(cursor.fetchall())

connection.commit()

cursor.close()
