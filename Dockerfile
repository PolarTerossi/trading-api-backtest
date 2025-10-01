# Usar uma imagem base oficial do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /code

# Copiar o arquivo de dependências para o diretório de trabalho
COPY ./requirements.txt /code/requirements.txt

# Instalar as dependências
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiar o código da aplicação para o diretório de trabalho
COPY ./app /code/app

# Comando para executar a aplicação quando o container iniciar
# Uvicorn vai rodar na porta 8000 e ficará acessível de fora do container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]