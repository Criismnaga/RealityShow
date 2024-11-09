from fastapi import APIRouter, HTTPException
from api.db import get_db_connection


router = APIRouter()


#* Obter um participante pelo username
@router.get("/participante/{username}", tags=["login"])
async def get_participante(username: str):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT participante_id FROM logins WHERE username = %s", (username,))
    participante = cursor.fetchone()

    cursor.close()
    connection.close()
    if not participante:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")
    return participante


#* Obter todos os participantes
@router.get("/logins", tags=["login"])
async def get_logins():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, participante_id, username FROM logins")
    logins = cursor.fetchall()

    cursor.close()
    connection.close()
    return logins
