# FEN-Alim 🚒

Bienvenue sur le dépôt GitLab du projet **FEN-Alim** !  
Ce projet est une application développée avec **React Native** et **Expo**.

Lien du projet : https://forgens.univ-ubs.fr/gitlab/but2info/fen-alim_a


## 📥 Récupérer le projet depuis Git

1. Pour commencer, récupérez l’application depuis GitLab (méthode SSH) :

   ```bash
   git clone git@forgens.univ-ubs.fr:but2info/fen-alim_a.git
   ```

2. Ensuite, déplacez-vous dans le projet :

   ```bash
   cd fen-alim_a
   ```

Voici l’arborescence du projet **FEN-Alim** :

```bash
fen-alim_a/
├─ backend/   (API + Base de données)
├─ fenalim/   (Application Front-End)
├─ README.md
```

## 📝 Guide GitLab

### 1. Mettre à jour vos fichiers locaux (pull)

```bash
git pull
```

### 2. Envoyer vos modifications sur GitLab (push)

```bash
git add .
git commit -m "COMMENTAIRE DU COMMIT"
git push
```


## 🚀 Lancer l’application

### 1 - Backend (API Docker)

1. Se déplacer dans le dossier backend :

   ```bash
   cd backend
   ```

2. Lancer l’API avec Docker :

   ```bash
   docker compose up -d --build
   ```

⚠️ Si vous souhaitez **réinstaller la base de données** (réinitialisation complète) :

```bash
docker compose down -v
```

---

### 2 - Frontend (Fenalim : React Native + Expo)

1. Se déplacer dans le dossier fenalim :

   ```bash
   cd fenalim
   ```

2. Démarrer l’application avec Expo Go :

   ```bash
   npx expo start
   ```

⚠️ Dans **/fenalim/app/(tabs)/accueil.tsx** : N’oubliez pas de **modifier l’adresse IP** et de mettre **la vôtre** !