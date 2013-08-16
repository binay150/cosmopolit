# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:


from DateTime import DateTime
from Log import Log
import json
from CacheDatabase import CacheDatabase
from NewsPaper import NewsPaper

_logger = Log.getLogger(__name__)

class NewspaperData(object):
    def __init__(self,):
        self.__newspaper_object = NewsPaper(
            CacheDatabase.get(NewsPaper)
        )

    def get_all_papers(self):
        papers = self.__newspaper_object.getAllPapers()
        return papers

    def get_paper(self, paper_id):
    	paper = self.__newspaper_object.getPaper(paper_id)
    	return paper