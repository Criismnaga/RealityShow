# Dockerfile-react
FROM node:16
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]

# Usar uma imagem base mais leve e específica
# FROM python:3.10-slim

# # Definir o diretório de trabalho
# WORKDIR /app

# # Instalar dependências do sistema necessárias para compilar pacotes como Pillow e numpy
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libjpeg-dev \
#     zlib1g-dev \
#     libpng-dev \
#     libopenblas-dev \
#     liblapack-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Copiar apenas o arquivo requirements.txt primeiro para otimizar o cache
# COPY requirements.txt .

# # Instalar dependências Python
# RUN pip install --no-cache-dir -r requirements.txt

# # Copiar o restante do código da aplicação
# COPY . .

# # Expor a porta padrão do Streamlit (se necessário)
# EXPOSE 8501

# # Comando para iniciar o Streamlit
# CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
