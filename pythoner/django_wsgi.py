import os,sys
sys.path.insert(0,'/www')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pythoner.settings'
import django.core.handlers.wsgi
application=django.core.handlers.wsgi.WSGIHandler()

