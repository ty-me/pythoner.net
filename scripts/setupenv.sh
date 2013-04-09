#!/bin/bash
yum install -y libmysqld-dev ibmysqlclient-dev,libfreetype
yum install -y libjpeg-devel freetype-devel libpng-devel
easy_install pip
install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv pythoner
workon pythoner
pip install -r requirements.txt
