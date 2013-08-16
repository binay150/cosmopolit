# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:

import re
import string
import copy
from Currency_v2 import Currency
from Database import Database, DatabaseObject
from Configuration import Configuration
from Constants import Constants
from Log import Log
import types
from DateTime import DateTime
_logger = Log.getLogger(__name__)

class NewsPaperDocument(DatabaseObject.Document):
    def __init__(self, document):
        DatabaseObject.Document.__init__(self, document)

    def getRealName(self):
        return self.data().get('real_name')

    def getActiveFlag(self):
        return self.data().get('active')

    def getLastUpdated(self):
        return self.data().get('last_updated')

    def getCountry(self):
        return self.data().get('country')

    def getUrl(self):
        return self.data().get('url')

    def getLanguage(self):
        return self.data().get('language')

    def getTimeStampRegistered(self):
        return self.data().get('timestamp_created')

    def getType(self):
        return self.data().get('type')

    def getImportancePoint(self):
        return self.data().get('importance')

    def getCeleryLock(self):
        return self.data().get('celery_lock')

    def activateCeleryLock(self):
        self.data()['celery_lock'] = True

    def turnOffCeleryLock(self):
        self.data()['celery_lock'] = False

    def deactivatePaper(self):
        self.data()['active'] = False

    def activatePaper(self):
        self.data()['active'] = True


class NewsPaper(DatabaseObject):
    def __init__(self, database):
        DatabaseObject.__init__(self, NewsPaperDocument, database,
                                Configuration.mobileBrandsDesignName())

    @staticmethod
    def database():
        return Database.newsPaper(
            server_connection_pool=True,
            server_cache_count_min=10,
            server_cache_count_max=75,
            db_cache=True,
        )

    def getPaper(self, news_paper_id):
        news_paper =  self.getObject(news_paper_id)
        if news_paper:
            return news_paper
        else:
            return None

    def does_the_paper_exist(self, news_paper_id):
        paper = self.get(news_paper_id)
        if paper:
            return True
        return False

    def registerNewspaper(self, paper_name, country, language, 
            url, real_name):
        assert (type(paper_name) == types.StringType or
                type(paper_name) == types.UnicodeType)
        assert type(country) == types.StringType
        assert type(url) == types.StringType
        assert type(real_name) == types.StringType
        assert type(language) == types.StringType
        #check if the paper name is already registered
        does_the_paper_id_exist = self.does_the_paper_exist(paper_name)
        assert not does_the_paper_id_exist 
        news_paper = self.getObject(None, create=True, values={
            '_id':paper_name,
            'url': url,
            'real_name': real_name,
            'language': language,
            'country': country,
            'timestamp_created': DateTime.utcNow(),
            'last_updated': DateTime.utcNow(),
        })
        if news_paper:
            news_paper.saveData()
            return news_paper
        assert False

    def getAllPapers(self):
        return self.getObjects()

    def delete(self, paper_name):
        self.__delitem__(paper_name)

    def getNewsPaper(self, brand_id):
        paper =  self.getObject(brand_id)
        if paper:
            return paper
        else:
            return None

    def getCountry(self, brand_id):
        doc = self.getObject(brand_id)
        if doc:
            return doc.data().country
        else:
            return None



