import mysql.connector
import os
import hashlib


#* Função para obter uma conexão com o banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "admin123"),
        database=os.getenv("DB_NAME", "fccpd"),
        port=int(os.getenv("DB_PORT", 3306))
    )


#* Função para gerar um hash da senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
