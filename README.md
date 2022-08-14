# Project 10 - API issues app

## Contents
- [Keywords](#keywords)
- [Description](#description)
- [Installation](#installation)
- [Use](#use)
- [Helpful links](#links)

## Keywords <a class="anchor" id="keywords"></a>
- Issue tracking system
- Author/Contributor
- Project
- Issue
- Comment


- Application Programming Interface (API) 
- Django Rest Framework (DRF)

## Description <a class="anchor" id="description"></a>

"Project 10 - API issues app" is a project of OpenClassrooms "Python Application Developer" 
course leading to a qualification.

This project aims to implement an API for an "Issue tracking system" using Django REST Framework.

The app allows users to create, read, update and delete (CRUD) projects/issues/comments 
and to add other users into a project as contributors.

The main functionalities of API are:
- Authenticate **users** during sign up and login.
- **Author users** can create/read/update/delete its projects/issues/comments.
- **Author users** can add **contributor users** into its projects.
- **Contributor users** can create issues into a project.
- **Contributor users** can read issues of a project.
- **Contributor users** can create comments into an issue.
- **Contributor users** can read comments of an issue.

The main technical requirements are:
- Create an API REST with Django Rest Framework (DRF).
- Implement authorization according to role of user (author/contributor).
- Comply OWASP standards.
- Create documentation in Postman.

You can also see technical documentation (French version) in 
`../p10_api_issues_app/documentation/`.

## Installation <a class="anchor" id="installation"></a>

Python version : 3.9.4

To get project, launch :
```
git clone https://github.com/edaucohe/p10_api_issues_app.git
```

To create virtual environment, go into the folder `../p10_api_issues_app/` and launch :
```
python -m venv env  
```

To activate virtual environment, launch :

- In windows
```
source env/Scripts/activate
```
- In Linux
```
source env/bin/activate
```

To install dependencies file `requirements.txt`, launch :
```
pip install -r requirements.txt
```

## Use <a class="anchor" id="use"></a>

To start API, go into the folder `../p10_api_issues_app/api/` and launch:
```
python manage.py runserver  
```

Concerning endpoints, they are formed by the root `http://127.0.0.1:8000/` followed by an URI. 
You can find here below the URI list:

| #   |    Functionality     | HTTP Request |                    URI                    |
|-----|:--------------------:|:------------:|:-----------------------------------------:|
| 1   |     User sign up     |     POST     |                 /signup/                  |
| 2   |      User login      |     POST     |                  /login/                  |
| 3   |   Display projects   |     GET      |                /projects/                 |
| 4   |   Create a project   |     POST     |                /projects/                 |
| 5   |  Display a project   |     GET      |              /projects/{id}/              |
| 6   |   Update a project   |     PUT      |              /projects/{id}/              |
| 7   |   Delete a project   |    DELETE    |              /projects/{id}/              |
| 8   |  Add a contributor   |     POST     |           /projects/{id}/users/           |
| 9   | Display contributors |     GET      |           /projects/{id}/users/           |
| 10  |  Delete contributor  |    DELETE    |         /projects/{id}/users/{id}         |
| 11  |    Display issues    |     GET      |          /projects/{id}/issues/           |
| 12  |   Create an issue    |     POST     |          /projects/{id}/issues/           |
| 13  |   Update an issue    |     PUT      |        /projects/{id}/issues/{id}         |
| 14  |   Delete an issue    |    DELETE    |        /projects/{id}/issues/{id}         |
| 15  |   Create a comment   |     POST     |    /projects/{id}/issues/{id}/comment/    |
| 16  |   Display comments   |     GET      |    /projects/{id}/issues/{id}/comment/    |
| 17  |   Update a comment   |     PUT      | /projects/{id}/issues/{id}/comment/{id}/  |
| 18  |   Delete a comment   |    DELETE    | /projects/{id}/issues/{id}/comment/{id}/  |
| 19  |  Display a comment   |     GET      | /projects/{id}/issues/{id}/comment/{id}/  |

So, when local server is launched, you can go to your Postman account and test endpoints 
according to API documentation (See [Helpful links](#links)).

## Helpful links <a class="anchor" id="links"></a>

DRF installation and settings:
https://www.django-rest-framework.org/

JWT installation and settings:
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html

Differences between APIView and ViewSet:
https://dev.to/koladev/apiview-vs-viewsets-4ln0

ViewSet methods exemples:
https://ilovedjango.com/django/rest-api-framework/views/viewset/

DRF Nested routers installation, explanation and exemples: 
https://github.com/alanjds/drf-nested-routers

API documentation: 
https://documenter.getpostman.com/view/22241212/VUjSGPdB
