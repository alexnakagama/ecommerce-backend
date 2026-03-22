FROM python:3.12-slim

WORKDIR /app

# Copia el archivo de dependencias
COPY pyproject.toml .

# Instala las dependencias directamente desde pyproject.toml
RUN pip install --upgrade pip && \
    pip install .

# Copia el resto del código
COPY . .

# Expone el puerto de FastAPI
EXPOSE 8000

# Inicia la app con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]