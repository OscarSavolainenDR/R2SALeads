A Django-based backend for my R2SA website. It services all of the front-end requests, and also interfaces with the Webscraper API to update the listings on a weekly basis.

It uses an AWS bucket for static storage of webscraped files. These are pushed to the bucket by the webscraper, and then an API call from the webscraper tells the backend to pull the files from the bucket.

It uses Mailtrap to automate emails to users, e.g. forgotten passwords.

For local development, it uses a PostgreSQL database. Therefore you will need some local PostgreSQL database: I used `pgAdmin 4`: https://www.pgadmin.org/.

In production, this backend was loaded onto a Heroku dyno, which has a built in database that automatically gets swapped in. The Heroku dyno also has a built-in REDIS broker.

Payments are done via Stripe (btw, Stripe has the best API documentation I have ever seen). This is mostly handled by the front end, but the backend has a webhook from Stripe that signals to the backend if a new customer has been created, their payments have succeeded, etc., so the backend can update their authorizations.

See `.example_env` for a list of required API/Secret keys, etc.


