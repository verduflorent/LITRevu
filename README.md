# LITRevu

LITRevu est une application web développée avec Django permettant à une communauté d'utilisateurs de demander et de publier des critiques de livres et d'articles.

Les utilisateurs peuvent notamment :

- créer un compte et se connecter ;
- publier des tickets pour demander une critique ;
- publier des critiques en réponse à des tickets ;
- créer simultanément un ticket et sa critique ;
- modifier ou supprimer leurs propres publications ;
- suivre et se désabonner d'autres utilisateurs ;
- consulter un flux personnalisé basé sur leurs abonnements ;
- consulter leurs propres publications et les réponses reçues.

## Prérequis

- Python 3
- Git

## Installation

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd LITRevu
```

### 2. Créer un environnement virtuel

Sous Windows PowerShell :

```powershell
python -m venv .venv
```

### 3. Activer l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Installer les dépendances

```powershell
pip install -r requirements.txt
```

## Lancement de l'application

Depuis la racine du projet :

```powershell
python manage.py runserver
```

Puis ouvrir dans un navigateur :

```text
http://127.0.0.1:8000/
```

## Base de données

Le projet utilise SQLite.

La base de données `db.sqlite3` est incluse dans le dépôt.

Les migrations peuvent être appliquées avec :

```powershell
python manage.py migrate
```

## Fonctionnalités principales

### Tickets

Un utilisateur peut créer un ticket pour demander une critique d'un livre ou d'un article. Un ticket peut contenir un titre, une description et une image.

### Critiques

Un utilisateur peut répondre à un ticket avec une critique comprenant un titre, une note de 0 à 5 et un commentaire.

### Flux

Le flux affiche les publications de l'utilisateur connecté, celles des utilisateurs qu'il suit ainsi que les critiques publiées en réponse à ses tickets.

Les publications sont affichées de la plus récente à la plus ancienne.

### Abonnements

Un utilisateur peut suivre d'autres utilisateurs et se désabonner afin de personnaliser son flux.

## Technologies utilisées

- Python
- Django
- SQLite
- HTML
- CSS
- Pillow

## Structure du projet

```text
LITRevu/
├── authentication/   # Authentification et utilisateurs
├── config/           # Configuration Django
├── media/            # Images envoyées par les utilisateurs
├── reviews/          # Tickets, critiques, abonnements et flux
├── db.sqlite3        # Base de données SQLite
├── manage.py
├── requirements.txt
└── README.md
```
