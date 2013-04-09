#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$DIR:$PYTHONPATH
export DJANGO_SETTINGS_MODULE="settings"
export ENV=$1
source /usr/local/bin/virtualenvwrapper.sh
workon pythoner

kill -9 `pgrep -f pythoner.sock`
sleep 0.5
uwsgi --daemonize /var/log/uwsgi_pythoner.log --socket /var/run/pythoner.sock --chmod-socket --module django_wsgi --pythonpath /www/pythoner --processes 6
