#!/bin/bash
sh env.sh
kill -9 `pgrep -f pythoner.sock`
sleep 0.5
uwsgi --daemonize /var/log/uwsgi_pythoner.log --socket /var/run/pythoner.sock --chmod-socket --module django_wsgi --pythonpath /www/pythoner --processes 6
