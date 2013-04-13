#encoding:utf-8
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
DOMAIN = 'http://pythoner.net'
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'pythoner_db',      
        'USER': 'root',               
        'PASSWORD': '',                
        'HOST': 'localhost',            
        'PORT': '',                      
        'REDIS': redis.Redis(host='127.0.0.1')
    }
}

ENV = os.getenv('ENV')
if ENV in ['DEV']:
    DEBUG = True
    DOMAIN = 'http://localhost:8000'


STATIC_ROOT = os.path.join(ROOT_PATH,'static')

TEMPLATE_DEBUG = DEBUG
TIME_ZONE = 'Asia/Shanghai'
DATETIME_FORMAT = 'Y-m-d H:i:s'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(ROOT_PATH,'media')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'fuck-gfw'

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
EMAIL_HOST = '******'
EMAIL_HOST_USER = '******'
EMAIL_HOST_PASSWORD = '******'

CACHE_BACKEND = 'file://'+os.path.join(ROOT_PATH,'cache')

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

PHOTO_SIZE = (128,128)
ICON_PHOTO_SIZE = (48,48)

DEFAULT_PASSWORD = '******'
DOUBAN_API_KEY = '******' 
DOUBAN_API_SECRET = '******' 
DOUBAN_SCOPE = 'shuo_basic_r,shuo_basic_w,douban_basic_common' 
DOUBAN_CALLBACK_URL = u'******'

WEIBO_APP_KEY = u'******'
WEIBO_APP_SECRET = u'******'
WEIBO_CALLBACK_URL = u'******'

TWITTER_APP_KEY = u'******'
TWITTER_APP_SECRET = u'******'
TWITTER_CALLBACK_URL = u'******'
