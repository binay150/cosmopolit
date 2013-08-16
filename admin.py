# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:

"""
Flask Blueprint for Sputnik that handles views for admin page only accessible
by members who have logged in with a jana.com google account
"""

# standard library
import csv
import datetime
import json
import sys
import tempfile
import traceback
from decimal import Decimal

# third party libraries
from flask import (
    Blueprint, current_app, session,
    render_template, redirect, url_for, flash,
    request,
    jsonify,
    Response
)
from Log import Log
import SharedExceptions as expectedex

# local libraries
_logger = Log.getLogger(__name__)
admin = Blueprint('admin', __name__)

@admin.route('/manage_papers')
def list_of_papers():
    papers = current_app.managers.papers.get_paper_lists()
    return render_template(
                            'paper_list.html', papers=papers
                        )

@admin.route('/manage_countries')
def list_of_countries():
    return render_template(
            'country_list.html'
        )

@admin.route('/manage_news_articles')
def news_articles():
    return render_template(
            'news_articles.html'
        )

@admin.route('/fetch_paper_detail', methods=['POST', 'GET'])
def fetch_paper_details():
    if request.method == 'GET':
        paper_id = request.args.get('paper_id')
        paper_details = current_app.managers.papers.get_paper_detail(paper_id)
        return jsonify(paper_details)

@admin.route('/activate_paper/<paper_id>')
def activate_paper(paper_id):
    try:
        current_status = current_app.managers.papers.activate_paper(paper_id)
        status_code = 200
    except expectedex.PaperAlreadyActive as e:
        current_status = 'fail'
        status_code = 404
    except expectedex.PaperNotFoundError as e:
        current_status = 'fail'
        status_code = 404
    response = jsonify({'status': current_status})
    response.status_code = status_code
    return response


