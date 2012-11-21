#!/bin/bash

/etc/init.d/nginx restart
sleep 0.5
/www/pythoner/uwsgi.sh
echo restarted
