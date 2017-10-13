Create a virtualenv::

  python3 -m venv env
  env/Scripts/pip install -U pip setuptools

Install dependencies::

  env/Scripts/pip install -r requirements.txt

Start a PostgreSQL or Mysql server::

  make db
  
Migrate database:
 flask db migrate

Start the server::

  env/bin/python wsgi.py or env/bin/python wsgi.py --reload


