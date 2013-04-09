#!/bin/bash
# for centos
yum  install -y libmysqld-dev ibmysqlclient-dev,libfreetype
easy_install pip
pip install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv pythoner
workon pythoner
pip install -r requirements.txt
yum install -y libjpeg-devel freetype-devel libpng-devel
