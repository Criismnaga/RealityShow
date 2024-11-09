from fastapi import FastAPI
from api.auth import router as auth_router
from api.participantes import router as participantes_router
from api.inscricoes import router as inscricoes_router
from api.db import get_db_connection


app = FastAPI()


#* Rota principal
@app.get("/")
def root():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    cursor.close()
    connection.close()
    return {"database": db_name}


#* Incluir as rotas dos outros arquivos
app.include_router(auth_router)
app.include_router(participantes_router)
app.include_router(inscricoes_router)
