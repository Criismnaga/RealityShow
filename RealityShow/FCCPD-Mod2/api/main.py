from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import hashlib
import os

app = FastAPI()

# Função para conectar ao banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "admin123"),
        database=os.getenv("DB_NAME", "fccpd"),
        port=int(os.getenv("DB_PORT", 3306))
    )

# Função para hash de senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Modelo de dados para cadastro
class RegisterData(BaseModel):
    username: str
    password: str
    nome: str
    email: str

# Endpoint para cadastro de usuário
@app.post("/register")
async def register(data: RegisterData):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Verificar se o username já existe na tabela logins
    cursor.execute("SELECT * FROM logins WHERE username = %s", (data.username,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="Username já cadastrado.")

    # Verificar se o email já existe na tabela participantes
    cursor.execute("SELECT * FROM participantes WHERE email = %s", (data.email,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    try:
        # Inserir dados do participante
        cursor.execute(
            "INSERT INTO participantes (nome, email) VALUES (%s, %s)",
            (data.nome, data.email)
        )
        participante_id = cursor.lastrowid

        # Inserir dados de login vinculados ao participante
        hashed_password = hash_password(data.password)
        cursor.execute(
            "INSERT INTO logins (participante_id, username, senha) VALUES (%s, %s, %s)",
            (participante_id, data.username, hashed_password)
        )

        connection.commit()
        return {"success": True, "message": "Usuário cadastrado com sucesso!"}

    except mysql.connector.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail="Erro ao registrar o usuário: {}".format(e))

    finally:
        cursor.close()
        connection.close()
