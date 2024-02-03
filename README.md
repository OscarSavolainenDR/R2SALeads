# R2SA Leads Website
A website I made for real-estate analysis. It webscrapes publicly availably to-rent listings and calculates their profitability as STLs based on surrounding comparables. It summarizes all of the results per listing that one can filter through, and provides a downloadable `.csv` file per listing with the full analysis per listing.

I don't really work on this anymore, but if anyone wants to grab it and use ot as the basis for anything, go ahead!

## Features:
### Frontend
The front-end is built in React and Tailwind CSS, based off of the Elstar template, as I am not a front-end expert by any stretch. It is fully integrated with Stripe payment APIs to take payments (btw, Stripe has the best API documentation I have ever seen). 

### Backend
This is a Django backend for my R2SA website. It services all of the front-end requests, and also interfaces with the Webscraper API to update the listings on a weekly basis.

#### AWS bucket for static storage
It uses an AWS bucket for static storage of webscraped files. These are pushed to the bucket by the webscraper, and then an API call from the webscraper tells the backend to pull the files from the bucket.

#### Mailtrap for automated handling of emails
It uses Mailtrap to automate emails to users, e.g. forgotten passwords.

#### PostgreSQL database
For local development, it uses a PostgreSQL database. Therefore you will need some local PostgreSQL database: I used `pgAdmin 4`: https://www.pgadmin.org/.

#### Celery for asynchronous message queues
You don't want to clog your backed with expensive computation, as I found was an issue with this app in processing a lot of the rela estate data. To make it all work, I had to spin up Celery workers to handle the computationally heavy stuff and not freeze the backend. Celery is an open-source asynchronous task queue, and I can highly recommend it, it was easy to use and worked like a charm!

#### We use Heroku dynos to host the backend in production
For production, I found Heroku to be a really neat and easy solution, it's a PaaS aand makes deploying apps super easy. Heroku also has a built-in database that automatically gets swapped in for the local database, and it has a built-in REDIS broker.

#### Integrated with Stripe payments via webhooks
The backed is also integrated with Stripe. The payments are mostly handled by the front end, but the backend has a webhook from Stripe that signals to the backend if a new customer has been created, their payments have succeeded, etc., so the backend can update their authorizations.


## Repo structure

### R2SA-frontend
This contains the frontend of the website, built in React and Tailwind CSS. See the [README](https://github.com/OscarSavolainenDR/R2SA_website/blob/main/R2SA-frontend/README.md) in the R2SA-frontend folder for more details. In production, it is simpler if this is made into a stand-alone git repo.

### R2SA-backend
The backend. Similarly to the front-end, in production it is simpler if this is made into a stand-alone git repo.
