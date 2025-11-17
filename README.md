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