FROM python:3.11-slim

# Éviter la création de fichiers .pyc et forcer l'affichage des logs Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installation de FFmpeg et dépendances système pour OpenCV/MediaPipe
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Dossier de travail
WORKDIR /app

# Copie des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste des fichiers
COPY . .
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Maintenir le conteneur actif pour le développement interactif
CMD ["tail", "-f", "/dev/null"]
