
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

"""
weibo API library
"""
__version__ = '1.5'
__author__ = 'Joshua Roesslein'
__license__ = 'MIT'

import sys
sys.path.insert(0,'/www/pythoner/others/apis')

from models import Status, User, DirectMessage, Friendship, SavedSearch, SearchResult, ModelFactory, IDSModel
from error import WeibopError
from api import API
from cache import Cache, MemoryCache, FileCache
from auth import BasicAuthHandler, OAuthHandler
from streaming import Stream, StreamListener
from cursor import Cursor

# Global, unauthenticated instance of API
api = API()

def debug(enable=True, level=1):

    import httplib
    httplib.HTTPConnection.debuglevel = level

