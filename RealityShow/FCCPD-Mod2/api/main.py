from fastapi import FastAPI, HTTPException
from typing import Any, Dict
from pydantic import BaseModel
import json
import mysql.connector
import hashlib
import os



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

class LoginData(BaseModel):
    username: str
    password: str

class InscricaoData(BaseModel):
    participante_id: int
    status: str = "Pendente"  # Valor padrão
    formulario: Dict[str, Any]

class UpdateInscricaoData(BaseModel):
    status: str
    


app = FastAPI()

# Rota para validar conexão com o banco de dados
@app.get('/')
def root():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    cursor.close()
    connection.close()
    return {"database": db_name}



#* Endpoint para cadastro de usuário
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


#* Endpoint para login
@app.post("/login")
async def login(data: LoginData):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Verificar se o usuário existe e obter a senha
    cursor.execute("SELECT * FROM logins WHERE username = %s", (data.username,))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Username não encontrado.")

    # Verificar a senha
    hashed_password = hash_password(data.password)
    if hashed_password != user["senha"]:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=401, detail="Senha incorreta.")

    # Fechar conexão após sucesso na verificação
    cursor.close()
    connection.close()

    # Retornar sucesso no login
    return {"success": True, "message": "Login realizado com sucesso!"}


#* Listar logins(menos o campo de senha)
@app.get("/logins")
async def get_logins():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Buscar todos os logins
    cursor.execute("SELECT id, participante_id, username FROM logins")
    logins = cursor.fetchall()

    # Fechar conexão e retornar logins
    cursor.close()
    connection.close()
    return logins


#* Get id pelo username
@app.get("/participante/{username}")
async def get_participante(username: str):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Buscar participante pelo username
    cursor.execute("SELECT participante_id FROM logins WHERE username = %s", (username,))
    participante = cursor.fetchone()

    # Fechar conexão e retornar participante
    cursor.close()
    connection.close()
    return participante


#* Criar inscrição
@app.post("/inscricao")
async def criar_inscricao(data: InscricaoData):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Verificar se o participante existe na tabela `participantes`
    cursor.execute("SELECT * FROM participantes WHERE id = %s", (data.participante_id,))
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Participante não encontrado.")

    # Inserir dados na tabela `inscricoes`
    cursor.execute(
        """
        INSERT INTO inscricoes (participante_id, status, formulario)
        VALUES (%s, %s, %s)
        """,
        (data.participante_id, data.status, json.dumps(data.formulario))
    )

    # Confirmar transação e fechar conexão
    connection.commit()
    inscricao_id = cursor.lastrowid
    cursor.close()
    connection.close()

    return {"success": True, "message": "Inscrição criada com sucesso", "inscricao_id": inscricao_id}


#* Atualizar inscrição 
@app.put("/inscricao/{inscricao_id}")
async def update_inscricao(inscricao_id: int, data: UpdateInscricaoData):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Verificar se a inscrição existe
    cursor.execute("SELECT * FROM inscricoes WHERE id = %s", (inscricao_id,))
    inscricao = cursor.fetchone()
    if not inscricao:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Inscrição não encontrada.")

    # Atualizar apenas o campo `status`
    cursor.execute(
        """
        UPDATE inscricoes 
        SET status = %s 
        WHERE id = %s
        """,
        (data.status, inscricao_id)
    )

    # Confirmar transação e fechar conexão
    connection.commit()
    cursor.close()
    connection.close()

    return {"success": True, "message": "Status da inscrição atualizado com sucesso"}



#* Listar inscrições
@app.get("/inscricoes")
async def get_inscricoes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Buscar todas as inscrições
    cursor.execute("SELECT * FROM inscricoes")
    inscricoes = cursor.fetchall()

    # Fechar conexão e retornar inscrições
    cursor.close()
    connection.close()
    return inscricoes


#* Delete inscrição
@app.delete("/inscricao/{inscricao_id}")
async def delete_inscricao(inscricao_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Verificar se a inscrição existe
    cursor.execute("SELECT * FROM inscricoes WHERE id = %s", (inscricao_id,))
    inscricao = cursor.fetchone()
    if not inscricao:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Inscrição não encontrada.")

    # Deletar inscrição
    cursor.execute("DELETE FROM inscricoes WHERE id = %s", (inscricao_id,))

    # Confirmar transação e fechar conexão
    connection.commit()
    cursor.close()
    connection.close()

    return {"success": True, "message": "Inscrição deletada com sucesso"}