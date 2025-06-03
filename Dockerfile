# Étape 1 : Utiliser une image légère mais complète
FROM python:3.10-slim

# Étape 2 : Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Étape 3 : Mettre à jour pip
RUN pip install --upgrade pip

# Étape 4 : Définir le répertoire de travail
WORKDIR /app

# Étape 5 : Copier les dépendances en premier pour optimiser le cache
COPY requirements.txt .

# Étape 6 : Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 7 : Copier le code source
COPY . .

# Étape 8 : Exposer le port (modifiable selon ton app)
EXPOSE 5000

# Étape 9 : Commande de lancement
CMD ["python", "app.py"]
