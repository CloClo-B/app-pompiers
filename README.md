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
  - Description détailler des points d'eau
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

| Nom Prénom | Email | Groupe |
|-----------|-------|--------|
| Clovis BOURRE | bourre.e2402184@etud.univ-ubs.fr | Gr2B |
| Mathéo BIET | biet.e2400505@etud.univ-ubs.fr | Gr2B |
| Valentin HUTA-CEVAER | huta-cevaer.e2402478@etud.univ-ubs.fr | Gr2B |
| Tei GARNIER | garnier.e2401205@etud.univ-ubs.fr | Gr2C |
| Clément HOARAU | hoarau.e2400553@etud.univ-ubs.fr | Gr2C |


## 📒 Documentation Notion

📌 **Lien vers le site Notion du projet** : https://fen-alim-a.notion.site/FEN-Alim-27eaa60e3d6581e6b773e16efbe575c4


## 🔗 Dépôt du projet

📌 **Lien GitLab** : https://forgens.univ-ubs.fr/gitlab/but2info/fen-alim_a



## 📁 Arborescence du projet

```bash
fen-alim_a/
├─ backend/   # API + Base de données
├─ fenalim/   # Application Frontend (React Native)
├─ README.md
```


## 🚀 Installation et Lancement

### 1. Cloner le dépôt
```bash
git clone https://forgens.univ-ubs.fr/gitlab/but2info/fen-alim_a.git
cd fen-alim_a
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
Avant de lancer l'application, il renseigné l'adresse IP de votre machine dans le fichier de configuration :
```
fenalim/config/api.ts    ← modifier l'IP ici
```
Remplacé l'IP par défaut par l'adresse IP locale de ta machine (ex: `192.168.1.XX`).

> 💡 Pour connaître votre IP : `ipconfig` (Windows) ou `ip a` (Linux/Mac)

### 5. Lancer l'application
```bash
npx expo start
```