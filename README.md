# Django 5.2.8 and DRF 3.16.1 Practice Project(November 2025)

## Requirements

* https://www.docker.com/
* https://code.visualstudio.com/

&nbsp;

# Getting Started

For your first time please run the next commands, if some new changes comes after a git pull please ask to the backend developer for the new changes available.


# Docker Network
## List all Docker networks
```
$ docker network ls
```

# Look for a line with NAME: watchmatenetwork
## Create a bridge network named watchmatenetwork

```
$ docker network create watchmatenetwork
```

# Basic Docker Compose commands

```
$ docker compose -f .\local.yml ps
$ docker compose -f .\local.yml up
$ docker compose -f .\local.yml build
$ docker compose -f .\local.yml down
```

```
$ docker compose -f .\test.yml up
```

# No Cache (If you have issues)
```
$ docker compose -f .\local.yml build --no-cache --progress=plain
```

# First Time Create DB
```
docker run --name drf_local_postgres `
  --env-file .\.envs\.local\.postgres `
  -p 5433:5432 `
  -v local_postgres_data:/var/lib/postgresql/data `
  --network watchmatenetwork `
  postgres:13.7
```

# Explore the container
```
$ docker ps
$ docker exec -it <container_id> bash
```


### Load Data Fixtures
```
$ docker compose -f .\local.yml run --rm django sh -c '/env/bin/python3 ./watchmate/manage.py migrate && /env/bin/python3 ./watchmate/manage.py loaddata watchmate/fixtures/*'
```

### This will create the tables
```
$ docker compose -f local.yml run --rm django python3 manage.py migrate
```

### Show volumes:

```
$ docker volume ls
```

### If you want to delete a Volume you have to down your compose configuration with docker-compose down, after that this should works:

```
$ docker volume rm <volumen>
```

### Or maybe you want to delete a docker image :

```
$ docker rm -f <image_name>
```

&nbsp;


### This will create the tables
```
$ docker-compose -f local.yml run --rm django python3 manage.py migrate
```
### Load the fixtures
Read the file fixtures.sh

### Create a local super user, please type the email & password for the super user
```
$ docker-compose -f local.yml run --rm django python3 manage.py createsuperuser
```

### Optional: If you want to create new migrations from models modifications or new models you can run the next command
```
$ docker-compose -f local.yml run --rm django python3 manage.py makemigrations users
```
&nbsp;

# Django Magic Stuff

### Django Extensions - Shell Plus usage

```
$ docker-compose -f local.yml run --rm django python3 manage.py shell_plus
```

### Individual images (For ipdb debugging)

```
$ docker-compose -f local.yml run --rm --service-ports django
```

&nbsp;


# PostgreSQL Connect

```
$ docker ps
$ docker exec -it <container_id> bash
$ su - postgres
$ psql postgresql://username:password@postgres:5432/watchmate_db
-- In PSQL Terminal show databases
psql=# \db
-- Use pg_global by id
psql=# use <database_id>
psql=#\dt
```

# Stop containers
```
$ docker stop $(docker ps -a -q)
```

# Delete all containers
```
$ docker rm $(docker ps -a -q)
```

OR
```
$ docker container prune -f
```

# Delete all Volumes
```
$ docker system prune --volumes
```

# Delete all images
```
$ docker rmi $(docker images -a -q)
```



# Windows Local Run

Activate Env
```
$ .\env\Scripts\activate 
```


```
Django Create Project
$ django-admin startproject watchmate
```


```
Django Create App
$ python manage.py startapp watchlist_app
```

```
Django Create SuperUser
$ python manage.py createsuperuser
```

```
Django Get UUID
$ python manage.py sqlmigrate watchlist_app 0004_alter_reviews_options_remove_reviews_id_reviews_uuid
```

```
Django Fake migration
python manage.py migrate watchlist_app 0004_alter_reviews_options_remove_reviews_id_reviews_uuid --fake
```

```
Movies Fixtures

python manage.py loaddata .\watchlist_app\fixtures\watchlists_200.json
```

```
Run all tests

python manage.py test
```

```
Only a bunch of tests grouped by TestCase

python manage.py test watchlist_app.tests.ReviewTestCase
```

```
Run individual test

python manage.py test watchlist_app.tests.WatchListTestCase.test_watchlist_create
```


# VSCode Debug File - launch.json

```
{
    "configurations": [
        {
            "name": "Containers: Python - Django",
            "type": "python",
            "request": "attach",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/watchmate",
                    "remoteRoot": "/app/watchmate"
                }
            ],
            "port": 3000,
            "host": "127.0.0.1"
            
        }
    ]
}
```