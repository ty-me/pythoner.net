#!/bin/bash
# for centos
yum  install -y libmysqld-dev ibmysqlclient-dev,libfreetype
yum  install -y libmysqld-dev ibmysqlclient-dev,libfreetype

easy_install virtualenv 
virtualenv /tmp/pythoner
. /tmp/pythoner/bin/activate

easy_install pip
pip install -r requirements.txt
