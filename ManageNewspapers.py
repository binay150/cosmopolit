# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:

from Newspapers.NewspaperData import NewspaperData
from Countries.CountriesData import CountriesData
from DateTime import DateTime
from Log import Log
import SharedExceptions as expectedex
import celery_tasks.fetch_news as fetch_news_celery_task
_logger = Log.getLogger(__name__)

class ManageNewspapers(object):

    def __init__(self):
        self.__newspaper_data = NewspaperData()
        self.__country_data = CountriesData()
    
    def get_paper_lists(self):
        papers = self.__newspaper_data.get_all_papers()
        papers_data = []
        for paper in papers:
        	country_id = paper.getCountry()
        	country = self.__country_data.getCountry(country_id)
        	country_name = country.getName()
        	papers_data.append({
        			'id': paper.key(),
        			'name': paper.getRealName(),
        			'updated': paper.getLastUpdated(),
        			'active': paper.getActiveFlag(),
        			'country': country_name
        		})
        
        return papers_data

    def get_paper_detail(self, paper_id):
    	paper = self.__newspaper_data.get_paper(paper_id)
    	if paper is None:
    		raise expectedex.PaperNotFoundError(
    			'paper_not_found'
    		)
    	details_to_return = {
    		'id': paper_id,
    		'name': paper.getRealName(),
    		'url': paper.getUrl(),
    		'language': paper.getLanguage(),
    		'registration_date': paper.getTimeStampRegistered(),
    		'last_updated': paper.getLastUpdated(),
    		'country': paper.getCountry(),
    		'type': paper.getType(),
    		'importance_point': paper.getImportancePoint(),
    		'active_flag': paper.getActiveFlag()
    	}
    	return details_to_return

    def activate_paper(self, paper_id):
        paper = self.__newspaper_data.get_paper(paper_id)
        if paper is None:
            _logger.debug('paper is None')
            raise expectedex.PaperNotFoundError(
                'paper_not_found'
            ) 
        #we do not want more than one celery task per paper
        #celery_lock helps us in achieving that
        celery_lock = paper.getCeleryLock()
        active_flag = paper.getActiveFlag()

        if active_flag:
            raise expectedex.PaperAlreadyActive(
                'a celery task still exists for the paper'
            )
        paper.activatePaper()
        if not celery_lock:
            fetch_news_celery_task.putPaperInQueue.apply_async(
                (paper_id,), queue='fetch_news'
            )








