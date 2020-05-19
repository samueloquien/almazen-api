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
