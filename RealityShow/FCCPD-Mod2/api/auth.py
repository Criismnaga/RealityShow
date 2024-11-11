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
    instagram: str
    seguidores: int

class LoginData(BaseModel):
    username: str
    password: str

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
        # Inserir dados na tabela participantes
        cursor.execute(
            "INSERT INTO participantes (nome, email, instagram, seguidores) VALUES (%s, %s,%s, %s)",
            (data.nome, data.email, data.instagram, data.seguidores)
        )
        participante_id = cursor.lastrowid

        # Inserir dados na tabela logins com a senha em texto simples
        cursor.execute(
            "INSERT INTO logins (participante_id, username, senha) VALUES (%s, %s, %s)",
            (participante_id, data.username, data.password)
        )
        connection.commit()
        return {"success": True, "message": "Usuário cadastrado com sucesso!"}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail="Erro ao registrar o usuário: {}".format(e))

    finally:
        cursor.close()
        connection.close()


@router.post("/login", tags=["login"])
async def login(data: LoginData):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Consulta para buscar o usuário e o nome do participante associado
    cursor.execute("""
        SELECT logins.id AS login_id, participantes.nome, logins.username, logins.senha
        FROM logins
        JOIN participantes ON logins.participante_id = participantes.id
        WHERE logins.username = %s
    """, (data.username,))
    user = cursor.fetchone()
    
    # Verificar se o usuário foi encontrado
    if not user:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")

    # Validação da senha como string simples
    if data.password != user["senha"]:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=401, detail="Senha incorreta.")

    # Fecha o cursor e a conexão após a consulta
    cursor.close()
    connection.close()

    # Retorna o ID, nome e nome de usuário do usuário logado
    return {
        "success": True,
        "message": "Login realizado com sucesso!",
        "id": user["login_id"],
        "nome": user["nome"],
        "username": user["username"]
    }
