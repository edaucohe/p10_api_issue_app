# Project 10 - API issues app

## Contents
- [Description](#description)
- [Installation](#installation)
- [Setup](#setup)
- [Use](#use)
- [Helpful links](#links)

## Description <a class="anchor" id="description"></a>

"Project 10 - API issues app" est un programme à réaliser dans le cadre de la formation diplômante d'OpenClassrooms "Développeur d'application Python".

Ce projet a comme but de mettre en place une application...


## Installation <a class="anchor" id="installation"></a>
    
Python version : 3.9

Pour récupérer le projet, lancez :
```
git clone https://github.com/edaucohe/p10_api_issues_app.git
```

Pour créer l'environnement virtuel, placez-vous dans le dossier `../projet9` et tapez :
```
python -m venv env  
```

Pour activer l'environnement virtuel, tapez :

- Sur windows
```
source env/Scripts/activate
```
- Sur Mac/Linux
```
source env/bin/activate
```

Pour installer les dépendances du fichier `requirements.txt`, lancez :
```
pip install -r requirements.txt
```

## Setup <a class="anchor" id="setup"></a>

Rien à signaler.

## Use <a class="anchor" id="use"></a>

Pour récupérer la base de données préalablement remplie, placez-vous dans le dossier `../projet9/merchex` et lancez :
```
python manage.py migrate  
```
Pour démarrer l'application, lancez :
```
python manage.py runserver  
```

Une fois le serveur local lancé, adressez-vous au lien du serveur local (voir [Helpful links](#links)) pour commencer à utiliser l'application.

Vous pouvez créer un nouvel utilisateur grâce au formulaire d'inscription. Néanmoins, la base de données est déjà remplie 
avec des utilisateurs fictifs. Vous trouverez ci-listée les coordonnées de ces utilisateurs fictifs :

| Nom d'utilisateur | Mot de passe |
|:-----------------:|:------------:|
|       anne        |    hianne    |
|       tony        |    hitony    |
|       john        |    hijohn    |
|       mari        |    himari    |

Vous pouvez aussi accéder au site d'administration en tant qu'administrateur,
il faut juste s'adresser au http://127.0.0.1:8000/admin/ et tapez les coordonnées ci-listées :

| Nom d'utilisateur | Mot de passe |
|:-----------------:|:------------:|
|       admin       |   hiadmin    |

Dans ce site, vous aurez l'affichage des objects sauvegardés dans la base de données.

Finalement, et afin d'arrêter le serveur local, tapez *ctrl + c* dans le terminal. 

## Helpful links <a class="anchor" id="links"></a>


