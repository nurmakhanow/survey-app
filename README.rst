Survey app
====
Build & run app

Build & run project use this command:

    $ docker-compose -f local.yml build
    $ docker-compose -f local.yml up
  

Create superuser:

    $ docker-compose -f local.yml exec django sh
    $ ./manage.py createsuperuser

In case you have trouble with ENV VAR try these:

    $ docker-compose -f local.yml run django sh
    $ ./manage.py createsuperuser

Admin:

* http://0.0.0.0:8000/admin
  
Swagger:

* http://0.0.0.0:8000/api/swagger/

Note!
------
Login to django-admin in order to use Swagger endpoints that require Authorization

Only users with 'is_survey_admin=True' are able to CRUD Surveys & Questions

'.envs' added to repo for convenience