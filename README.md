# 📊 Plateforme de Gestion et d'Analyse des Données de l’INPC (Projet ANSADE)

## 📝 Description

La plateforme **ANSADE** est une application **web** développée en **Django** pour la gestion et l'analyse des **données de l’Indice National des Prix à la Consommation (INPC)**.  
Elle permet de collecter, traiter et visualiser les données des produits et des prix en Mauritanie, facilitant ainsi la prise de décision statistique.

---

## 🏗️ Architecture du Projet

### 🖥️ Backend
- **Framework** : Django (Python)
- **Base de Données** : PostgreSQL
- **API REST** : Django REST Framework (DRF)
- **Gestion des tâches** : Celery (Asynchrones)

### 🎨 Frontend
- **Technologies** : React.js / Vue.js (optionnel)
- **Visualisation de Données** : Chart.js / D3.js

### 🗄️ Stockage des Données
- **Base relationnelle** : PostgreSQL pour structurer les données.
- **Stockage fichiers** : AWS S3 (ou local pour l'import/export Excel).

### 🔒 Sécurité & Authentification
- **JWT (JSON Web Token)** pour les sessions utilisateurs.
- **Gestion des permissions avancée** (administrateur, analyste, utilisateur).

### 🚀 Déploiement
- **Conteneurisation** : Docker
- **Orchestration** : Docker Compose / Kubernetes
- **Hébergement** : AWS, Google Cloud ou Azure

---

## 🎯 Fonctionnalités Clés

### ✅ Gestion des Données
- **Import / Export** de fichiers **Excel/CSV**.
- **Système de validation automatique** des données.
- **Journalisation et historique des modifications**.

### 📊 Analyse et Visualisation
- **Calcul de l’INPC mensuel et annuel**.
- **Analyse comparative des prix par région**.
- **Graphiques interactifs et tableaux de bord**.

### 📄 Génération de Rapports
- **Rapports PDF & Excel** générés automatiquement.
- **Personnalisation des rapports** (produits, régions, périodes…).

### 🛒 Gestion des Produits et des Prix
- **Ajout, modification et suppression** de produits et de leurs prix.
- **Suivi des tendances de prix** et des évolutions.

### 📌 Gestion des Utilisateurs et Permissions
- **Authentification sécurisée avec JWT**.
- **Attribution de rôles et permissions** par utilisateur.

---

## 🛠️ Technologies Utilisées

| Technologie | Usage |
|------------|-------|
| **Django** | Backend |
| **Django REST Framework** | API REST |
| **PostgreSQL** | Base de données |
| **Celery** | Tâches asynchrones |
| **Chart.js / D3.js** | Visualisation des données |
| **Docker** | Conteneurisation |
| **JWT** | Authentification |

---

## 🔧 Installation et Déploiement

### 📦 Prérequis
- **Docker** et **Docker Compose** installés sur votre machine.
- **Python 3.12** ou plus récent.
- **PostgreSQL** (si non utilisé en conteneur).

### 🏗️ Démarrage du projet

#### 🔹 1️⃣ Cloner le projet
```sh
git clone https://github.com/utilisateur/projet-ansade.git
cd projet-ansade
```
#### 🔹 2️⃣ Démarrer les services avec Docker
```sh
docker compose up -d --build
docker compose start or restart
