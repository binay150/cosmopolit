# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:

import re
import string
import copy
from Database import Database, DatabaseObject
from Configuration import Configuration
from Constants import Constants
from Log import Log
import types
from DateTime import DateTime
_logger = Log.getLogger(__name__)

class NewsCounterDocument(DatabaseObject.Document):
    def __init__(self, document):
        DatabaseObject.Document.__init__(self, document)

class NewsCounter(DatabaseObject):
    def __init__(self, database):
        DatabaseObject.__init__(self, NewsCounterDocument, database,
                                Configuration.news_counterDesignName())

    @staticmethod
    def database():
        return Database.news_counter(
            server_connection_pool=True,
            server_cache_count_min=10,
            server_cache_count_max=75,
            db_cache=True,
        )

    def getLastIndex(self):
        count =  self.getObject('news_counter')
        if count:
            return count.data().count
        else:
            return None

    def increaseCounter(self):
        count =  self.getObject('news_counter')
        count_val = count.data().count
        int_count = int(count_val)+1
        count_template = ('000000000000'+str(int_count))[-12:]
        count.data().count = count_template

    def appendNewsIdto(self, news_id, databasetype):
        repo =  self.getObject(databasetype)         
        if repo: 
            current_list = repo.data().current_list
            current_list.append(news_id)
        else:
            current_list = [news_id]
            self.getObject(None, create=True, values={
            '_id':databasetype,
            'current_list':current_list,
            'last_updated': DateTime.utcNow(),
            })
