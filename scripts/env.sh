#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$DIR:$PYTHONPATH
export DJANGO_SETTINGS_MODULE="settings"
export ENV=$1
. /tmp/pythoner/bin/activate
