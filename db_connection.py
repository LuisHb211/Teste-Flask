import mysql.connector
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def get_db_connection():
    try:
        # Obtém os valores das variáveis de ambiente
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        database = os.getenv("DATABASE")

        # Estabelece a conexão com o banco de dados MySQL
        connection = mysql.connector.connect(user=user, password=password, host=host, database=database)
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {str(e)}")
        return None