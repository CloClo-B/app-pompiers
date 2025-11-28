FROM python:3.12-slim

#Définit le répertoire de travail.
WORKDIR /app

#Récupère les dépendances python.
COPY requirements.txt .

#Installe les dépendances sans cache pour alléger.
RUN pip install --no-cache-dir -r requirements.txt

#Copie /app dans le conteneur.
COPY app ./app

#Commande exécutée lors du lancement du conteneur.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
