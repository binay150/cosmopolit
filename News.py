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

class NewsDocument(DatabaseObject.Document):
    def __init__(self, document):
        DatabaseObject.Document.__init__(self, document)


class News(DatabaseObject):
    def __init__(self, database):
        DatabaseObject.__init__(self, NewsDocument, database,
                                Configuration.newsDesignName())

    @staticmethod
    def database():
        return Database.news(
            server_connection_pool=True,
            server_cache_count_min=10,
            server_cache_count_max=75,
            db_cache=True,
        )

    def get(self, news_id):
        news =  self.getObject(news_id)
        if news:
            return news
        else:
            return None

    def does_the_news_exist(self, url):
        val = self.getObject(
            view='by_news_url',
            key=url,
        )
        if val:
            return True
        return False

    def registerNews(self, news_data):
        assert type(news_data['paper_name']) == types.StringType or type(news_data['paper_name']) == types.UnicodeType
        assert type(news_data['paper_url']) == types.StringType or type(news_data['paper_url']) == types.UnicodeType
        assert type(news_data['link']) == types.StringType or type(news_data['link']) == types.UnicodeType
        assert type(news_data['title']) == types.UnicodeType or type(news_data['title']) == types.StringType
        assert type(news_data['summary_detail']) == types.StringType or type(news_data['summary_detail']) == types.UnicodeType or news_data['summary_detail'] is None
        #check if the paper name is already registered
        does_the_news_exist = self.does_the_news_exist(news_data['link'])
        assert not does_the_news_exist
        news = self.getObject(None, create=True, values=news_data)
        if news:
            news.saveData()
            return True
        assert False

    def getAllBrands(self):
        return self.getObjects()

    def delete(self, paper_name):
        self.__delitem__(paper_name)

    def getNews(self, brand_id):
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



