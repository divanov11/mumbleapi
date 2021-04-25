#
<p align="center">
<img src="./static/images/Mumble-logo.png" width="20%">
</p>

<div align="center">
<h1>Welcome to the Mumble Api Repository !</h1>

</div>

<br/>

## Getting Started 

If you are trying to use this project for the first time, you can get up and running by following these steps. 

> ⚠ Note, this step assumes you are using **github ssh keys** for the *git clone method*
<br/>

## Requirements 

|Technology|Version|
|:--:|:--:|
|**Python**|**3.x**|
|**pip**|**latest version**|
|**asgiref**|**3.3.4**|
|**Django**|**3.2**|
|**django-cors-headers**|**3.7.0**|
|**djangorestframework**|**3.12.4**|
|**djangorestframework-simplejwt**|**4.6.0**|
|**gunicorn**|**20.1.0**|
|**Pillow**|**8.2.0**|
|**PyJWT**|**2.0.1**|
|**pytz**|**2021.1**|
|**sqlparse**|**0.4.1**|
|**whitenoise**|**5.2.0**|

## Running

Make sure you have **Python 3.x** installed and **the latest version of pip** *installed* before running these steps.

- `git clone git@github.com:divanov11/mumbleapi.git`
- `cd mumbleapi`
- `python3 -m venv env`
- `source env/Scripts/activate`
- `pip install -r requirements.txt`
- `python manage.py runserver`


> ⚠ If everything is good and has been done successfully, your **Django Rest API** should be hosted on port 8000.  