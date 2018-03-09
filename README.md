# assignment

## Setup the DB
- createdb plivodb
- PGOPTIONS='--client-min-messages=warning' psql -X -q -1 -v ON_ERROR_STOP=1 --pset pager=off -d plivodb -f testdatadump.sql -L restore.log
 
## Run Redis Server
- sudo apt-get install redis-server
- redis-server

## Setup and run the Server
- virtualenv -p python3 env
- source env/bin/activate
- pip install django
- pip install psycopg2-binary
- pip install redis
- cd sms_service/

#### Add DB Details in settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'plivodb',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
#### Add Redis Server Details in settings.py
```
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = '0'
```
- python manage.py runserver

