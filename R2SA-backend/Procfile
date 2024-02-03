
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn backend_v3.wsgi --log-file -
celery: celery -A backend_v3 worker -l info -c 4
