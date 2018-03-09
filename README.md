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
- python manage.py runserver

