Create a virtualenv::

  python3 -m venv env
  env/Scripts/pip install -U pip setuptools

Install dependencies::

  env/Scripts/pip install -r requirements.txt

Start a PostgreSQL or Mysql server::

  make db
  
Migrate database if you change db:
 flask db migrate
and upgrade with new change
 flassk db upgrade


Start the server::

  env/bin/python wsgi.py or env/bin/python wsgi.py --reload


