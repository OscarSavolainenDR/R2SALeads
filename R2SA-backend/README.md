# A Django backend for my R2SA website
It services all of the front-end requests, and also interfaces with the Webscraper API to update the listings on a weekly basis.

## Features

### AWS bucket for static storage
It uses an AWS bucket for static storage of webscraped files. These are pushed to the bucket by the webscraper, and then an API call from the webscraper tells the backend to pull the files from the bucket.

### Mailtrap for automated handling of emails
It uses Mailtrap to automate emails to users, e.g. forgotten passwords.

### PostgreSQL database
For local development, it uses a PostgreSQL database. Therefore you will need some local PostgreSQL database: I used `pgAdmin 4`: https://www.pgadmin.org/.

### Celery for asynchronous message queues
You don't want to clog your backed with expensive computation, as I found was an issue with this app in processing a lot of the rela estate data. To make it all work, I had to spin up Celery workers to handle the computationally heavy stuff and not freeze the backend. Celery is an open-source asynchronous task queue, and I can highly recommend it, it was easy to use and worked like a charm!

### We use Heroku dynos to host the backend in production
In production, this backend was loaded onto a Heroku dyno, which has a built in database that automatically gets swapped in. The Heroku dyno also has a built-in REDIS broker.

### Integrated with Stripe payments via webhooks
Payments are done via Stripe (btw, Stripe has the best API documentation I have ever seen). This is mostly handled by the front end, but the backend has a webhook from Stripe that signals to the backend if a new customer has been created, their payments have succeeded, etc., so the backend can update their authorizations.

<br>

## To get started:

ToDo.

An issue is that I have to create detailed documentation on how to set up the webscraper, AWS bucket, or just spin this up myself and post photos.

<!--
I will assume you have cloned the parent directory, which is the "root" of the git repo. To start up a local development server, first install the dependencies. It is best to do this inside of a conda environment.

Once inside a dedicated conda environment, run:
```
pip install -r local_requirements.txt
```

Then, to start up a local development server, one can run:
```
python manage.py runserver
```

This will not work, as the database has not been configured. First, install a PostgreSQL client, and initialize a database. Then, in `backend_v3` create an `.env` file and populate it with the database variables. See `backend_v3/.example_env` for a list of required API/Secret keys, etc.

Finally, one also has to create an AWS sotrage bucket
-->




