#
<div align="center">
<img src="./static/images/dark-logo.1c6c40e2.png" width="20%">
<h1>Welcome to the Mumble Api Repository</h1>

<a href="https://discord.gg/TxgpyK8pzf">![Mumble Community](https://img.shields.io/discord/825371211399692308?label=Mumble%20Community&style=for-the-badge&logo=Discord)</a>
<a href="http://mumbleapi.herokuapp.com/">![Mumble](https://img.shields.io/badge/Mumble-API-9cf?style=for-the-badge)</a>

</div>

<br/>

## Getting Started 

If you are trying to use this project for the first time, you can get up and running by following these steps. 

To contribute to this project, please see the [contributing guidelines](https://github.com/divanov11/mumbleapi/blob/master/Contributing.md).
> ⚠ Note, this step assumes you are using **github ssh keys** for the *git clone method*

<a align="center" href="https://drawsql.app/dennis-ivy/diagrams/mumble">

<img width="80%" align="center" src="./img/drawSQL-MumbleApi.png"/>

</a>

## Requirements 

|Technology|Version|
|:--:|:--:|
|**Python**|**3.x**|
|**pip**|**latest version**|
|**asgiref**|**3.3.4**|
|**dj-database-url**|**0.5.0**|
|**Django**|**3.2**|
|**django-cors-headers**|**3.7.0**|
|**django-heroku**|**0.3.1**|
|**djangorestframework**|**3.12.4**|
|**djangorestframework-simplejwt**|**4.6.0**|
|**gunicorn**|**20.1.0**|
|**Pillow**|**8.2.0**|
|**psycopg2**|**2.8.6**|
|**PyJWT**|**2.0.1**|
|**pytz**|**2021.1**|
|**six**|**1.15.0**|
|**sqlparse**|**0.4.1**|
|**whitenoise**|**5.2.0**|


## Running

Make sure you have **Python 3.x** installed and **the latest version of pip** *installed* before running these steps.

-> Clone the repository using the following command
```bash
git clone git@github.com:divanov11/mumbleapi.git
# After cloning, move into the directory having the project files using the change directory command
cd mumbleapi
```
-> Now create a virtual environment where all the required python packages will be installed
```bash
# Use this on Windows
py -3 -m venv env
# Use this on Linux and Mac
python -m venv env
```
-> Activate the virtual environment
```bash
# Windows
.\env\Scripts\activate
# Linux and Mac
source env/bin/activate
```
-> Install all the project Requirements
```bash
pip install -r requirements.txt
```
-> Finally, run the django development server
```bash
# apply migrations and create your database
python manage.py migrate

# Create a user with manage.py
python manage.py createsuperuser

# load data for feed
python manage.py loaddata feeddata.json

# load data for article
python manage.py loaddata articledata.json

# load data for discussion
python manage.py loaddata discussiondata.json

# run django development server
python manage.py runserver
```

## Explore admin panel for model data or instances
http://127.0.0.1:8000/admin or http://localhost:8000/admin

## Login with the user credentials you just created using createsuperuser command

<br />

> ⚠ If everything is good and has been done successfully, your **Django Rest API** should be hosted on port 8000 i.e http://127.0.0.1:8000/ or http://localhost:8000/  
