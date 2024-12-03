from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
import redis
import os
import openai
from transformers import pipeline  # Para usar o modelo preditivo local

# Configurar OpenAI com chave de API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configurar MongoDB
mongo_uri = os.getenv("MONGO_URI")
# Conectar ao MongoDB com a variável mongo_uri

# Configurar Redis
redis_host = os.getenv("REDIS_HOST", "localhost")  # Valor padrão para Redis
redis_port = os.getenv("REDIS_PORT", 6379)        # Valor padrão para Redis
redis_db = os.getenv("REDIS_DB", 0)               # Valor padrão para Redis

# Conectando ao MongoDB
try:
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client["meu_banco"]
    collection = db["interacoes"]
    print("Conectado ao MongoDB com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")

# Conectando ao Redis
try:
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    redis_client.ping()
    print("Conectado ao Redis com sucesso!")
except redis.ConnectionError as e:
    print(f"Erro ao conectar ao Redis: {e}")

# Inicializando o FastAPI
app = FastAPI()

# Carregando o modelo preditivo local (pode ser GPT-2 ou outro modelo de linguagem leve)
predictor = pipeline('text-generation', model='gpt2')

# Modelos de dados
class UserInput(BaseModel):
    pergunta: str

class Feedback(BaseModel):
    pergunta: str
    resposta: str
    util: bool
    comentario: str = None

# Função para obter resposta localmente
def gerar_resposta_local(pergunta: str):
    # Gerando resposta com o modelo preditivo local (GPT-2 ou similar)
    resposta = predictor(pergunta, max_length=150, num_return_sequences=1)[0]['generated_text']
    return resposta.strip()

# Função para consultar a OpenAI quando necessário
def consultar_openai(pergunta: str):
    try:
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou outro modelo de chat como gpt-4
            messages=[
                {"role": "system", "content": "Você é um assistente inteligente."},
                {"role": "user", "content": pergunta}
            ]
        )
        resposta = openai_response["choices"][0]["message"]["content"].strip()
        return resposta
    except Exception as e:
        return "Desculpe, houve um erro ao tentar processar sua pergunta."

# Rota principal para receber perguntas
@app.post("/perguntar/")
def perguntar(input: UserInput):
    pergunta = input.pergunta

    # Verifica se a resposta está em cache no Redis
    resposta_cache = redis_client.get(pergunta)
    if resposta_cache:
        resposta = resposta_cache.decode("utf-8")
    else:
        # Verifica no MongoDB se já existe uma resposta
        resposta_db = collection.find_one({"pergunta": pergunta})
        if resposta_db:
            resposta = resposta_db["resposta"]
        else:
            # Usando o modelo preditivo local (se não encontrar no cache ou banco)
            resposta = gerar_resposta_local(pergunta)

            # Caso o modelo local não forneça uma resposta satisfatória, consulta a OpenAI
            if not resposta:
                resposta = consultar_openai(pergunta)

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
    try:
        mongo_status = "OK" if mongo_client.server_info() else "Erro"
    except Exception as e:
        mongo_status = f"Erro: {e}"

    redis_status = "OK" if redis_client.ping() else "Erro"

    return {"mongo": mongo_status, "redis": redis_status}

# Rodando o servidor FastAPI se for o script principal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
