#!/bin/bash
# for centos
yum  install -y libmysqld-dev ibmysqlclient-dev,libfreetype
easy_install pip
pip install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv pythoner
workon pythoner
yum install -y libjpeg-devel freetype-devel libpng-devel
pip install -r requirements.txt
