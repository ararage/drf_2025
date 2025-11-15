# Windows

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

