# Usando imagem oficial do Python
FROM python:3.9-slim

# Definindo diretório de trabalho
WORKDIR /app

# Copiando arquivos para o contêiner
COPY requirements.txt .

# Instalando dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código da aplicação
COPY . .

# Expondo a porta
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
