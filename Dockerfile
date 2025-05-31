FROM python:3.10-slim

# Installer dépendances système utiles
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installer pip et mises à jour
RUN pip install --upgrade pip

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier le code dans le conteneur
COPY . /app

# Installer les dépendances Python du projet
RUN pip install -r requirements.txt

# Exposer le port de l'application (ex: 5000 pour Flask)
EXPOSE 5000

# Lancer l'application (modifie selon ton point d'entrée)
CMD ["python", "main.py"]
