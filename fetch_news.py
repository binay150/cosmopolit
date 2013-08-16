# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:

import os
import InitializeConfiguration
from Configuration import Configuration
os.environ['CELERY_CONFIG_MODULE'] = Configuration.celeryNewsPaperConfigModule()

from celery.task import task
from celery import Task
from DateTime import DateTime
from Log import Log
import json
from CacheDatabase import CacheDatabase
from NewsPaper import NewsPaper
from NewsCounter import NewsCounter
from News import News
from CeleryLibs.FetchNews import FetchNews
from 

_logger = Log.getLogger(__name__)

class DatabaseTask(Task):
    _newspaper_object = None
    _news_object = None
    _newscounter_object = None
    _rediscounter = None

    @property
    def newsPaper(self):
        if self._newspaper_object is None:
            self._newspaper_object = NewsPaper(
                    CacheDatabase.get(NewsPaper)
                )
        return self._newspaper_object

    @property
    def news(self):
        if self._news_object is None:
            self._news_object = News(
                    CacheDatabase.get(News)
                )
        return self._news_object

    @property
    def newsCounter(self):
        if self._newscounter_object is None:
            self._newscounter_object = NewsCounter(
                    CacheDatabase.get(NewsCounter)
                )
        return self._newscounter_object

    @property 
    def redisCounter(self):
        if self._rediscounter is None:
            self._rediscounter = NewsCounter(
                                                   CacheDatabase.get(NewsCounter)
                                                   )
        return self._rediscounter


@task(base=DatabaseTask)
def putPaperInQueue(paper_id):
    _logger.debug('this is the queue')
    try:
        fetch_news = FetchNews(
            putPaperInQueue.newsPaper,
            putPaperInQueue.news,
            putPaperInQueue.newsCounter,
            putPaperInQueue,
        )
        fetch_news.fetchNews(paper_id)
    except:
        _logger.exception('Something unexpected happened')



