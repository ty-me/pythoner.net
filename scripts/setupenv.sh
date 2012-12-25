#!/bin/bash
sudo apt-get install -y libmysqld-dev ibmysqlclient-dev
sudo easy_install pip
sudo pip install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv pythoner
workon pythoner
pip install -r requirements.txt
