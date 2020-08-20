# almazen-api
Python API to the almazen service


### Run server

``` PowerShell
/path/to/virtual/environment/Scripts/activate.ps1
cd path/to/almazen-api
python manage.py runserver
```



### Update DB

* python manage.py db init  (only once)
* python manage.py db migrate
* python manage.py db upgrade


### Run tests

``` PowerShell
python -m behave -k --no-capture
python -m behave --tags=@wip -k --no-capture
```
