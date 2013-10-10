#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.ORG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import redis

ROOT_PATH = os.path.normpath(os.path.dirname(__file__)).replace('\\','/')
DEFAULT_CHARSET = 'utf8'

ADMINS = (
    ('admin', 'admin@pythoner.net'),
)

MANAGERS = ADMINS

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SITE_NAME = 'site name'
DOMAIN = 'http://pythoner.net'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'pythoner_db',      
        'USER': 'username',               
        'PASSWORD': 'password',                
        'HOST': 'localhost',            
        'PORT': '',                      
        'REDIS': redis.Redis(host='127.0.0.1')
    }
}

ENV = os.getenv('ENV')

if ENV in ['DEV','DEBUG']:
    DEBUG = True
else:
    DEBUG = False

STATIC_ROOT = os.path.join(ROOT_PATH,'static')

TEMPLATE_DEBUG = DEBUG
TIME_ZONE = 'Asia/Shanghai'
DATETIME_FORMAT = 'Y-m-d H:i:s'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(ROOT_PATH,'media')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '***'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pythoner.utils.middlewares.PreventWatering',
    'pythoner.utils.middlewares.XsSharing',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'pythoner.urls'

TEMPLATE_DIRS = (
   os.path.join(ROOT_PATH,'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.comments',
    'wiki',
    'home',
    'books',
    'accounts',
    'main',
    'pm',
    'topic',
    'code',
    'link',
    'jobs',
    'utils',
    'south',
)

USE_TZ = False

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

CACHE_BACKEND = 'file://'+os.path.join(ROOT_PATH,'cache')

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

PHOTO_SIZE = (128,128)
ICON_PHOTO_SIZE = (48,48)

DEFAULT_PASSWORD = '******'

DOUBAN_API_KEY = '' 
DOUBAN_API_SECRET = '' 
DOUBAN_SCOPE = 'shuo_basic_r,shuo_basic_w,douban_basic_common' 
DOUBAN_CALLBACK_URL = u'http://pythoner.net/accounts/login/douban/callback/'

WEIBO_APP_KEY = u''
WEIBO_APP_SECRET = u''
WEIBO_CALLBACK_URL = u'http://pythoner.net/accounts/login/sina/callback/'
