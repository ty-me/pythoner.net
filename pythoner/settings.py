#encoding:utf-8
import os
import socket
import redis

ROOT_PATH = os.path.normpath(os.path.dirname(__file__)).replace('\\','/')
DEFAULT_CHARSET = 'utf8'

ADMINS = (
    ('admin', 'admin@pythoner.net'),
)

MANAGERS = ADMINS

# 本地环境
if socket.gethostname() in ['ubuntu','bogon','ty-ubuntu','pro.local']:
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    DEBUG = True
    DOMAIN = 'http://local.pythoner.net'
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
# 服务器环境
else:
    SESSION_ENGINE	= 'django.contrib.sessions.backends.cache'
    DEBUG = False
    DOMAIN = 'http://pythoner.net'
    DATABASES = {
        'default': {

            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'pythoner_db',     
            'USER': 'pythoner',            
            'PASSWORD': 'XWb6VmRRhuUqT8nc', 
            'HOST': 'localhost',                      
            'PORT': '',                      
            'REDIS': redis.Redis(host='127.0.0.1')
        }
    }

TEMPLATE_DEBUG = DEBUG
TIME_ZONE = 'Asia/Shanghai'
DATETIME_FORMAT = 'Y-m-d H:i:s'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(ROOT_PATH,'media')

if DEBUG:
    STATIC_ROOT = os.path.join(ROOT_PATH,'static')
else:
    STATIC_ROOT = '/var/pythoner.net/static/' # nginx

MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '#x99xnv(!c-ip@e*@0sbpc$jxb+x!%bfw3f-1c0hi@$%moz+y@'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',  # 去掉这行
    'django.middleware.csrf.CsrfResponseMiddleware', # must before ViewMiddle
    #'CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
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
    'search',
    'main',
    'pm',
    'topic',
    'code',
    'link',
    'jobs',
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'xxx@gmail.com'
EMAIL_HOST_PASSWORD = '******'

if DEBUG: 
    CACHE_BACKEND = 'file://'+os.path.join(ROOT_PATH,'cache')
else:
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
    #CACHE_BACKEND = 'file://'+os.path.join(ROOT_PATH,'cache')

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

PHOTO_SIZE = (128,128)
ICON_PHOTO_SIZE = (48,48)
DEFAULT_PASSWORD = '********'

DOUBAN_API_KEY = '******' 
DOUBAN_API_SECRET = '******' 
DOUBAN_SCOPE = 'shuo_basic_r,shuo_basic_w,douban_basic_common' 
DOUBAN_CALLBACK_URL = u'http://pythoner.net/accounts/login/douban/callback/'

WEIBO_APP_KEY = u'******'
WEIBO_APP_SECRET = u'******'
WEIBO_CALLBACK_URL = u'http://pythoner.net/accounts/login/sina/callback/'


