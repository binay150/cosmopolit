#!/usr/bin/env python
# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:

from DateTime import DateTime
from Log import Log
import feedparser

_logger = Log.getLogger(__name__)

class FetchNews(object):
    def __init__(self, newspaper_object, news_object, 
                newscounter_object, celery_fetch_news_task,
                rediscounter):
        self.__newspaper = newspaper_object
        self.__news = news_object
        self.__newscounter = newscounter_object
        self.__rediscounter = rediscounter
        self.__celery_fetch_news_task = celery_fetch_news_task

    def fetchNews(self, paper_id):
        paper = self.__newspaper.getPaper(paper_id)
        active_flag = paper.getActiveFlag()
        if not active_flag:
            paper.turnOffCeleryLock()
            return None
        else:
            paper.activateCeleryLock()
        url = paper.getUrl()
        try:
            data = feedparser.parse(url)
            entries =  data.entries
            for entry in entries:
                #TODO record news here
                #increase counters in redis
                _logger.debug(entry)
            self._putPaperInQueue(paper_id)
        except:
            paper.turnOffCeleryLock()
            paper.deactivatePaper()
            _logger.exception('someting weird happened')

    def _putPaperInQueue(self, paper_id):            
        datetime_pending = datetimetz.utcnow() + timedelta(
                    minutes=10,
                )
        self.__celery_fetch_news_task.apply_async(
                (paper_id,), queue='fetch_news', eta=datetime_pending
            )