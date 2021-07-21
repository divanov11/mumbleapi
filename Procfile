web: gunicorn mumblebackend.wsgi --log-file -
release: python manage.py migrate
release: python manage.py migrate --database=message