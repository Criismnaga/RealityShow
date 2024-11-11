from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.db import get_db_connection


router = APIRouter()


class InscricaoData(BaseModel):
    participante_id: int
    idade: int
    apellido: str
    animal: str
    habilidades: str
    estacao: str
    musica: str

class UpdateInscricaoData(BaseModel):
    status: str


#* Criar uma inscrição
@router.post("/inscricao", tags=["user"]) 
async def criar_inscricao(data: InscricaoData):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM participantes WHERE id = %s", (data.participante_id,))
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Participante não encontrado.")

    cursor.execute(
        "INSERT INTO inscricoes (participante_id, idade, apelido_colegio, animal_representa, habilidade, estacao_ano, musica_preferida) VALUES",
        (data.participante_id, data.idade, data.apellido, data.animal, data.habilidades, data.estacao, data.musica)
    )
    connection.commit()
    inscricao_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {"success": True, "message": "Inscrição criada com sucesso", "inscricao_id": inscricao_id}


#* Atualizar o status da inscrição
@router.put("/inscricao/{inscricao_id}", tags=["admin"])
async def update_inscricao(inscricao_id: int, data: UpdateInscricaoData):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inscricoes WHERE id = %s", (inscricao_id,))
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Inscrição não encontrada.")

    cursor.execute("UPDATE inscricoes SET status = %s WHERE id = %s", (data.status, inscricao_id))
    connection.commit()
    cursor.close()
    connection.close()
    return {"success": True, "message": "Status da inscrição atualizado com sucesso"}


#* Listar todas as inscrições
@router.get("/inscricoes", tags=["admin"])
async def get_inscricoes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT participantes.id AS participante_id, participantes.nome AS nome_participante, inscricoes.* FROM inscricoes JOIN participantes ON inscricoes.participante_id = participantes.id;")
    inscricoes = cursor.fetchall()
    cursor.close()
    connection.close()
    return inscricoes


#* Listar inscrições aprovadas
@router.get("/inscricoes/aprovados", tags=["admin"])
async def get_inscricoes_aprovadas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT participantes.id AS participante_id, participantes.nome AS nome_participante, inscricoes.* FROM inscricoes JOIN participantes ON inscricoes.participante_id = participantes.id; WHERE inscricoes.status = 'Aprovado'")
    inscricoes = cursor.fetchall()
    cursor.close()
    connection.close()
    return inscricoes


#* Deletar uma inscrição específica
@router.delete("/inscricao/{inscricao_id}", tags=["user"])
async def delete_inscricao(inscricao_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inscricoes WHERE id = %s", (inscricao_id,))
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Inscrição não encontrada.")

    cursor.execute("DELETE FROM inscricoes WHERE id = %s", (inscricao_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"success": True, "message": "Inscrição deletada com sucesso"}
