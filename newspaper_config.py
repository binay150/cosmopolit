# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:

import sys, os
_root = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)[:-1]
sys.path.extend([
    os.path.sep.join(_root + ['ThirdParty']),
    os.path.sep.join(_root + ['Configuration']),
    os.path.sep.join(_root + ['Common']),
    os.path.sep.join(_root + ['DB']),
    os.path.sep.join(_root + ['Library']),
    os.path.sep.join(_root)
])
import InitializeConfiguration
from Configuration import Configuration
import urlparse


redis_url = Configuration.celeryNewsPaperRedisUrl()
redis_info = urlparse.urlsplit(redis_url)

CELERY_IMPORTS = (
    'celery_tasks.fetch_news',
)

BROKER_URL = redis_url

CELERY_RESULT_BACKEND = 'redis'
CELERYD_LOG_LEVEL = Configuration.logFileLevel().upper()
CELERY_SEND_EVENTS = True
CELERYD_POOL = 'eventlet'
CELERYD_CONCURRENCY = 500
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = {
    'default': {
        'exchange': 'default',
        'routing_key': 'default'
    },
    'fetch_news': {
        'exchange': 'fetch_news',
        'routing_key': 'fetch_news',
    }
}
