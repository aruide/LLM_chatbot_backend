FROM python:3.10

# Installer les dépendances système nécessaires à la compilation
RUN apt-get update && apt-get install -y \
    build-essential \
   && rm -rf /var/lib/apt/lists/*

# Mettre à jour pipAdd commentMore actions
RUN pip install --upgrade pip

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt en premier (optimisation du cache Docker)
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Copier le reste du code dans le conteneur
COPY . /app

# Exposer le port 5000 (ou autre selon ton application)
EXPOSE 5000

# Commande pour lancer l'application (modifie selon ton point d'entrée)
CMD ["python", "main.py"]
