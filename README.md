# FEN-Alim 🚒

Bienvenue sur le dépôt Git du projet **FEN-Alim**.

Ce projet s’inscrit dans le cadre de la **lutte contre les feux d’espaces naturels**, où un accès rapide, fiable et sécurisé aux points d’eau est un enjeu majeur pour l’efficacité des secours.


## 📌 Présentation du projet

Lors d’un incendie en milieu naturel, les pompiers doivent pouvoir localiser rapidement des points d’eau fonctionnels (hydrants, points d’eau naturels, réserves privées). Or, ces informations sont souvent dispersées, obsolètes ou difficiles d’accès, ce qui peut ralentir considérablement les interventions.

Le projet **FEN-Alim** vise à répondre à cette problématique en développant une **application mobile Android et iOS**, connectée à un **serveur central**, destinée aux pompiers et aux acteurs concernés.


## 🎯 Objectifs de l’application

L’application FEN-Alim permet :

- 📍 **Le suivi et la gestion des points d’eau**  
  - Coordonnées GPS  
  - Débit  
  - Type de raccordement  
  - État de fonctionnement  
  - Date de dernière vérification  
  - Photos  

- 🗺️ **La visualisation cartographique**
  - Localisation des points d’eau
  - Description détaillée des points d'eau
  - Calcul de l'itinéraire

- 👥 **Une gestion multi-niveaux des accès**
  - Public
  - Pompier
  - Commandement
  - Admin

Les citoyens peuvent notamment :
- Signaler des anomalies (fuite, casse, obstruction…)


## 🔐 Sécurité

Les échanges entre l’application mobile et le serveur sont sécurisés grâce à :
- Une **API protégée**
- L’utilisation de **certificats SSL**, garantissant la confidentialité et l’intégrité des données


## 🛠️ Technologies utilisées

- **Frontend** : React Native + Expo  
- **Backend** : API + Base de données (Docker)  
- **Plateformes** : Android & iOS  


## 👋 Équipe du projet

| Nom Prénom |
|-----------|
| Clovis BOURRE (SCRUM MASTER) |
| Mathéo BIET |
| Valentin HUTA-CEVAER |
| Tei GARNIER |
| Clément HOARAU |


## 📒 Documentation Notion

📌 **Lien vers le site Notion du projet** : https://www.notion.so/clovis-bourre/FEN-Alim-BUT2-349c6649422b807a8c2df1cd98d93f67



## 📁 Arborescence du projet

```bash
app-pompiers/
├─ backend/   # API + Base de données
├─ fenalim/   # Application Frontend (React Native)
├─ README.md
```


## 🚀 Installation et Lancement

### 1. Cloner le dépôt
```bash
git clone https://github.com/CloClo-B/app-pompiers.git

cd app-pompiers
```

### 2. Lancer le backend (Docker)
```bash
docker compose up --build -d
```

### 3. Installer les dépendances frontend
```bash
cd fenalim
npm install
```

### 4. Configuration de l'adresse IP
Avant de lancer l'application, il faut renseigné l'adresse IP de votre machine dans le fichier de configuration :
```
fenalim/config/api.ts    ← modifier l'IP ici
```
Remplacé l'IP par défaut par l'adresse IP locale de votre machine (ex: `192.168.1.XX`).

> 💡 Pour connaître votre IP : `ipconfig` (Windows) ou `ip a` (Linux/Mac)

### 5. Lancer l'application
```bash
npx expo start
```
