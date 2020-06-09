# CUSTOM REST API
This project implements a custom api with a custom authentication method.

## Get Ready
### Basic programs you need for the commands to work
- Any shape or form to download this repository into you desired folder
```
git clone https://github.com/SamiUrias/master_devel_testing_api.git
```
- Pipenv: I use pipenv to create and manage  my virtualenv, then  I am going to explain how to make this project
run using pipenv.
- Postgresql (DBMS):  I choose postgres for this project, despite the fact that django can handle multiple databases I
strongly suggest to use postgres to smoothly follow this readme.


## Setup
- Install all the dependencies in your virtual environment.

```
pipenv install
```


- Create a new postgres database
- Modify the `/api/settings.py` in the database section with your database configuration
- Run the following command to activate the shell of pipenv
```
pipenv shell
```
- Apply all the migrations
```
python manage.py migrate
```
- Run the development server
```
python manage.py runserver
```


## Versions
### General
Dendencies that will be installed once the project is started

| Package | Version |
|:-------------:|:-----:|
|asgiref|3.2.7|
|Django|3.0.7|
|djangorestframework|3.11.0|
|importlib-metadata|1.6.1|
|Markdown|3.2.2|
|psycopg2|2.8.5|
|pytz|2020.1|
|sqlparse|0.3.1|
|zipp|3.1.0|

## Alternative Install
### General
I left a `requirements.txt` file in the project if you want to use a conventional installation using `vevnv`.
- Create a new virtual environment
```
virtualenv venv
```
- Activate the environment
```
source /venv/bin/activate
```
- Install all the dependencies
```
pip install -r requirements.txt
```
- Apply all the migrations
```
python manage.py migrate
```
- Run the development server
```
python manage.py runserver
```
