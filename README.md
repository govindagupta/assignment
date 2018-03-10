# assignment


## Setup API Server
- virtualenv -p python3 env
- source env/bin/activate
- pip install django
- pip install psycopg2-binary
- pip install redis
- cd sms_service/

#### Setup Redis Server

Run Redis Server
- sudo apt-get install redis-server
- redis-server

Add Redis Server Details in settings.py as following
```
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = '0'
```
#### Setup the DB

Create the DB
- createdb testdb

Add DB Details in settings.py as following
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testdb',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
- python manage.py makemigrations
- python manage.py migrate

After migration, DB should be populated with following command
- PGOPTIONS='--client-min-messages=warning' psql -X -q -1 -v ON_ERROR_STOP=1 --pset pager=off -d testdb -f testdatadump.sql -L restore.log

Finally run the API server
- python manage.py runserver

