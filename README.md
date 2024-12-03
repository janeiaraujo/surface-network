# Surface-Network: Uma IA Descentralizada e Autônoma
O Surface-Network é uma inteligência artificial totalmente autônoma, projetada para funcionar de forma descentralizada sem depender de APIs externas. Utilizando tecnologias como Python, MongoDB, Redis e contêineres Docker, ela oferece aprendizado contínuo e captura de feedback dos usuários para melhorar suas respostas ao longo do tempo.

## 🛠️ Tecnologias Utilizadas
* Python: Linguagem principal para o desenvolvimento da IA.
* Flask: Framework web para a criação da API REST.
* MongoDB: Banco de dados NoSQL para armazenamento de documentos, interações e dados de aprendizado.
* Redis: Utilizado para caching, melhorando a performance do sistema.
* Docker: Para containerização da aplicação e de seus serviços.
* OpenAI (Opcional): Integração para respostas pré-treinadas enquanto a IA desenvolve seu próprio modelo.
## 🌟 Funcionalidades

* Respostas Dinâmicas: Gera respostas baseadas em aprendizado contínuo.
* Captura de Feedback: O usuário pode avaliar a utilidade das respostas para melhorar o modelo.
* Pipeline de Dados: Automatiza o processo de re-treinamento com base nas interações.
* Totalmente Descentralizada: Funciona localmente sem depender de serviços externos, garantindo autonomia total.
## 📂 Estrutura de Diretórios

````
surface-network/
│
├── app/
│   ├── main.py               # Arquivo principal da aplicação Flask
│   ├── models/               # Modelos para NLP e aprendizado
│   ├── utils/                # Funções auxiliares
│   ├── static/               # Arquivos estáticos (CSS, JS)
│   └── templates/            # Templates HTML para a interface web (opcional)
│
├── data/
│   └── datasets/             # Datasets públicos para o pré-treinamento
│
├── Dockerfile                # Dockerfile para construção do contêiner
├── docker-compose.yml        # Arquivo de configuração do Docker Compose
├── requirements.txt          # Dependências da aplicação
└── .env                      # Arquivo de variáveis de ambiente
````

## ⚙️ Configuração do Ambiente

1. Clonar o Repositório

````
git clone https://github.com/seu-usuario/surface-network.git
cd surface-network
````

1. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto e adicione suas configurações:

````

OPENAI_API_KEY=your_openai_api_key_here
MONGO_URI=mongodb://mongodb:27017/my_database
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
````

3. Construir e Executar os Contêineres
Utilize o Docker Compose para construir e rodar os serviços:

````

docker-compose up --build
````

## 🚀 Uso da Aplicação
Acessar a API
A aplicação estará disponível em http://localhost:5000.

Interagir com a IA
Você pode fazer requisições POST para o endpoint /ask:

````

curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d '{"question": "Qual é a capital da França?"}'
````

Feedback
A resposta incluirá uma opção para fornecer feedback útil ou não.

### 🔄 Aprendizado Contínuo
O Surface-Network captura cada interação e a avalia com base no feedback do usuário. O processo de aprendizado contínuo ocorre com re-treinamento periódico baseado nos dados coletados.

Treinamento Manual (opcional)
Se desejar realizar o treinamento manual, utilize o script de treinamento:

bash
````
python app/train.py
````

🛡️ Contribuição
Sinta-se à vontade para abrir issues e enviar pull requests. Toda contribuição será bem-vinda!

📄 Licença
Este projeto está licenciado sob a MIT License.

🌐 Links Úteis
* Documentação do Flask: Flask
* Documentação do MongoDB: MongoDB
* Documentação do Redis: Redis


Com o Surface-Network, sua IA estará preparada para aprender e evoluir de forma totalmente independente! 🎯