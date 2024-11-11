from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.db import get_db_connection

router = APIRouter()

class InscricaoData(BaseModel):
    participante_id: int
    idade: int
    apelido_colegio: str
    animal_representa: str
    habilidade: str
    estacao_ano: str
    musica_preferida: str

class UpdateInscricaoData(BaseModel):
    status: str

#* Criar uma inscrição
@router.post("/inscricao", tags=["user"]) 
async def criar_inscricao(data: InscricaoData):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Verifica se o participante existe
    cursor.execute("SELECT * FROM participantes WHERE id = %s", (data.participante_id,))
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Participante não encontrado.")

    # Cria a inscrição
    cursor.execute(
        """
        INSERT INTO inscricoes 
        (participante_id, idade, apelido_colegio, animal_representa, habilidade, estacao_ano, musica_preferida) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (data.participante_id, data.idade, data.apelido_colegio, data.animal_representa, data.habilidade, data.estacao_ano, data.musica_preferida)
    )
    connection.commit()
    inscricao_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {"success": True, "message": "Inscrição criada com sucesso", "inscricao_id": inscricao_id}

#* Obter inscrição por ID do participante
@router.get("/inscricao/{participante_id}", tags=["user"])
async def get_participant_by_id_endpoint(participante_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM inscricoes WHERE participante_id = %s", (participante_id,))
        participant = cursor.fetchone()

        if not participant:
            raise HTTPException(status_code=404, detail="Participante não encontrado.")

        return participant

    finally:
        cursor.close()
        connection.close()

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
    cursor.execute("""
        SELECT participantes.id AS participante_id, participantes.nome AS nome_participante, inscricoes.* 
        FROM inscricoes 
        JOIN participantes ON inscricoes.participante_id = participantes.id
    """)
    inscricoes = cursor.fetchall()
    cursor.close()
    connection.close()
    return inscricoes

#* Listar inscrições aprovadas
@router.get("/inscricoes/aprovados", tags=["admin"])
async def get_inscricoes_aprovadas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT participantes.id AS participante_id, participantes.nome AS nome_participante, inscricoes.* 
        FROM inscricoes 
        JOIN participantes ON inscricoes.participante_id = participantes.id
        WHERE inscricoes.status = 'Aprovado'
    """)
    inscricoes = cursor.fetchall()
    cursor.close()
    connection.close()
    return inscricoes

@router.delete("/inscricao/{inscricao_id}", tags=["user"])
async def delete_inscricao(inscricao_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Verifica se a inscrição existe
        cursor.execute("SELECT * FROM inscricoes WHERE id = %s", (inscricao_id,))
        inscricao = cursor.fetchone()
        if not inscricao:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada.")
        
        # Obtém o participante_id associado à inscrição
        participante_id = inscricao['participante_id']

        # Deleta a inscrição da tabela `inscricoes`
        cursor.execute("DELETE FROM inscricoes WHERE id = %s", (inscricao_id,))

        # Deleta o login associado ao participante da tabela `logins`
        cursor.execute("DELETE FROM logins WHERE participante_id = %s", (participante_id,))

        # Deleta o participante da tabela `participantes`
        cursor.execute("DELETE FROM participantes WHERE id = %s", (participante_id,))

        # Confirma as deleções
        connection.commit()

        return {"success": True, "message": "Inscrição e dados associados deletados com sucesso"}

    except Exception as e:
        connection.rollback()  # Reverte em caso de erro
        raise HTTPException(status_code=500, detail=f"Erro ao deletar inscrição: {str(e)}")

    finally:
        cursor.close()
        connection.close()