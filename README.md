# shortener

### Setup

1. Install poetry https://python-poetry.org/
2. Create and install packages (steps described at poetry site)
3. Run migrations for project:

```
python manage.py migrate
```

4. Runserver:

```
python manage.py runserver
```

5. Post URL to shorten. Endpoint:

```
http://127.0.0.1:8000/api/v1/aliased-url/
```

6. Try out shortened url
