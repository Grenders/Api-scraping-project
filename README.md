A Django application project with APIs for working with character data, scraping, asynchronous tasks, and tests. The following technologies were used
1. Django - A web framework for creating the backend, including models, views, and routes.
2. Django REST Framework (DRF) - A library for creating RESTful APIs used for data serialization (and processing HTTP requests).
3. Celery - A framework for asynchronous task processing used for periodic synchronization with the API.
4. drf-spectacular - Library for automatic generation of OpenAPI documentation for APIs.
5. requests - A library for executing HTTP requests used for scraping data from an external API.
6. PostgreSQL - A database used by the Django ORM to store models.


## How to run
- Create venv: `python -m venv venv`
- Activate it `venv/bin/aactivate`
- Install requirements.txt `pip install -r requirements.txt`
- Run migrations `python manage.py migrate`
- Run Redis server `docker run -d -p 6379:6379 redis`
- Run celery worker for tasks  `celery -A config worker --loglevel=info`
- Run celery beat for tash  `celery -A config beat --loglevel=info`
- Create schedule for running sync in DB
- Run app: `python manage.py runserver` 