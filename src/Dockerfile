# Basierend auf dem offiziellen Python-Image
FROM python:3.11-slim-bullseye

# Arbeitsverzeichnis im Container setzen
WORKDIR /app


COPY requirements.txt .

# Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

#Alle  Projektdateien in den Container kopieren
COPY . .


# Den Port freigeben

EXPOSE 8501

# Starte die Streamlit App direkt mit dem Python-Interpreter
CMD ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
