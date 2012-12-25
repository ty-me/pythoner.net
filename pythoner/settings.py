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


# 本地环境
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
DEBUG = True
DOMAIN = 'localhost:8009'
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

if ENV in ['DEV','TY']:
    DEBUG = True
    pass
else:
    pass


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
    'main',
    'pm',
    'topic',
    'code',
    'link',
    'jobs',
)

EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = 'tianyu0915@qq.com'
EMAIL_HOST_PASSWORD = 'tyzxwdtys'

CACHE_BACKEND = 'file://'+os.path.join(ROOT_PATH,'cache')

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

PHOTO_SIZE = (128,128)
ICON_PHOTO_SIZE = (48,48)

DEFAULT_PASSWORD = '122126382'
DOUBAN_API_KEY = '09762ab58aac6baa1c628020a00542fe' 
DOUBAN_API_SECRET = '57d35048a51dfb5d' 
DOUBAN_SCOPE = 'shuo_basic_r,shuo_basic_w,douban_basic_common' 
DOUBAN_CALLBACK_URL = u'http://pythoner.net/accounts/login/douban/callback/'

WEIBO_APP_KEY = u'3589637735'
WEIBO_APP_SECRET = u'2b8b95f3f2ab0f562a3f67752213e0d8'
WEIBO_CALLBACK_URL = u'http://pythoner.net/accounts/login/sina/callback/'

TWITTER_APP_KEY = u'3589637735'
TWITTER_APP_SECRET = u'2b8b95f3f2ab0f562a3f67752213e0d8'
TWITTER_CALLBACK_URL = u'http://pythoner.net/accounts/login/sina/callback/'
