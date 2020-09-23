#!/bin/sh
. /var/pythonVM3/bin/activate
uwsgi --ini /var/django/django_demo/mysite_uwsgi.ini  # the --ini option is used to specify a file
deactivate
