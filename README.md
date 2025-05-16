# Personal Budget Tracker App

# Command  to Create  an Django Project

1. django-admin startproject pbta_backend 
2. cd pbta_backend 
3. python  manage.py startapp app

# Start the Django  Server
4. python  pbta_backend/manage.py runserver

## This  command  we  nees to run everytime  we  make  changes  to  the models.
1. python  pbta_backend/manage.py makemigrations

## Inorder to apply  the migrations  ...
1. python  pbta_backend/manage.py migrate

## Get the tree of  the directory
1. tree -I '__pycache__'

##
1.gunicorn --chdir pbta_backend pbta_backend.wsgi:application