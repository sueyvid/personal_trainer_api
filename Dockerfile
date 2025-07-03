# Usa imagem oficial Python
FROM python:3.11-slim

# Cria diretório de trabalho
WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY ./app ./app

# Expõe a porta
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
