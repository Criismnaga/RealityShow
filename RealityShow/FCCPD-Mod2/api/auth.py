from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mysql.connector
from api.db import get_db_connection, hash_password


router = APIRouter()


class RegisterData(BaseModel):
    username: str
    password: str
    nome: str
    email: str

class LoginData(BaseModel):
    username: str
    password: str


#* Registrar um novo usuário
@router.post("/register", tags=["cadastro"])
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
        cursor.execute(
            "INSERT INTO participantes (nome, email) VALUES (%s, %s)",
            (data.nome, data.email)
        )
        participante_id = cursor.lastrowid
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


#* Realizar login
@router.post("/login", tags=["login"])
async def login(data: LoginData):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM logins WHERE username = %s", (data.username,))
    user = cursor.fetchone()
    
    if not user or hash_password(data.password) != user["senha"]:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=401, detail="Credenciais incorretas.")

    cursor.close()
    connection.close()
    return {"success": True, "message": "Login realizado com sucesso!"}
