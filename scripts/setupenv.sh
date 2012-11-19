#!/bin/bash
sudo apt-get -y install mysql-server,python,python-dev,nginx,redis-server,python-setuptools
sudo easy_install pip
sudo pip install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv pythoner
workon pythoner
pip install -r requirements.txt
