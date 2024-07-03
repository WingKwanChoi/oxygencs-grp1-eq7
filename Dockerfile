# Utiliser une image de base Python
FROM python:3.8-slim

# Définir le répertoire de travail
WORKDIR /app

# Empêche Python d'écrire des fichiers pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Empêche Python de mettre en mémoire tampon stdout et stderr
ENV PYTHONUNBUFFERED=1

# Variables d'environnement spécifiques à l'application
ENV HOST=http://159.203.50.162
ENV TOKEN=999109532408abf795f3
ENV T_MAX=25
ENV T_MIN=18
ENV PG_USER=user01eq7
ENV PG_HOST=157.230.69.113
ENV PG_DATABASE=db01eq7
ENV PG_PASSWORD=nJCxUQQGEzAYKnWw
ENV PG_PORT=5432
#ENV DB_URL=...

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source
COPY . .

# Exposer le port sur lequel l'application écoute
EXPOSE 8001

# Commande pour lancer l'application
CMD ["python", "src/main.py"]
