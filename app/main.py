from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
import redis
import os
import openai


# Configurar OpenAI com chave de API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configurar MongoDB
mongo_uri = os.getenv("MONGO_URI")
# Conectar ao MongoDB com a variável mongo_uri

# Configurar Redis
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_db = os.getenv("REDIS_DB")
# Conectar ao Redis com essas variáveis

# Conectando ao MongoDB
mongo_client = MongoClient(mongo_uri)
db = mongo_client["meu_banco"]
collection = db["interacoes"]

# Conectando ao Redis
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

# Inicializando o FastAPI
app = FastAPI()

# Modelos de dados
class UserInput(BaseModel):
    pergunta: str

class Feedback(BaseModel):
    pergunta: str
    resposta: str
    util: bool
    comentario: str = None

# Rota principal para receber perguntas
@app.post("/perguntar/")
def perguntar(input: UserInput):
    pergunta = input.pergunta

    # Verifica se a resposta está em cache no Redis
    resposta_cache = redis_client.get(pergunta)
    if resposta_cache:
        resposta = resposta_cache.decode("utf-8")
    else:
        try:
            # Predição usando o modelo local
            resposta = model.predict([pergunta])[0]
        except Exception:
            # Consultar a OpenAI quando não houver uma resposta local
            openai_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Responda a esta pergunta: {pergunta}",
                max_tokens=150
            )
            resposta = openai_response["choices"][0]["text"].strip()
            resposta = f"Ainda estou aprendendo! Consultei na OpenAI esta resposta: {resposta}"

        # Cacheando a resposta no Redis
        redis_client.set(pergunta, resposta)

    # Salvando interação no MongoDB
    collection.insert_one({"pergunta": pergunta, "resposta": resposta})

    return {"pergunta": pergunta, "resposta": resposta}

# Rota para receber feedback
@app.post("/feedback/")
def feedback(data: Feedback):
    result = collection.update_one(
        {"pergunta": data.pergunta, "resposta": data.resposta},
        {"$set": {"feedback": data.util, "comentario": data.comentario}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Interação não encontrada.")

    return {"message": "Feedback recebido com sucesso!"}

# Rota para listar interações salvas
@app.get("/interacoes/")
def listar_interacoes(skip: int = 0, limit: int = Query(default=10, lte=100)):
    interacoes = list(collection.find().skip(skip).limit(limit))
    for interacao in interacoes:
        interacao["_id"] = str(interacao["_id"])  # Convertendo ObjectId para string
    return {"interacoes": interacoes}

# Rota para testar conexão com o MongoDB e Redis
@app.get("/health/")
def health_check():
    mongo_status = "OK" if mongo_client.server_info() else "Erro"
    redis_status = "OK" if redis_client.ping() else "Erro"
    return {"mongo": mongo_status, "redis": redis_status}
