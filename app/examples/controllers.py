# -*- coding: utf-8 -*-
from os import path
import logging
logger = logging.Logger(__name__)

from flask import render_template, session, g, send_from_directory, request
from app import app
from flask_login import login_required, current_user

from app.examples import blueprint, sentiment_pipeline

@blueprint.route('/example/sentiment-analysis', methods=['GET', 'POST'])
#@login_required
def sentiment_analysis():


    if request.method == 'GET':
        return render_template('examples/sentiment-analysis.html', config=app.config, text_value='', sentiment_result='')
    
    # if request.method == 'POST'
    text_value = request.form.get('text_area')

    print(text_value)
    sentiment_predict = sentiment_pipeline([text_value])
    score = sentiment_predict[0]['score']
    if sentiment_predict[0]['label']=='POSITIVE':
        result = f'<i class="fa-solid fa-face-smile" style="color:orange; font-size: 50px;"></i> Positive: {round(score, 3)*100}%'
    elif sentiment_predict[0]['label']=='NEGATIVE':
        result = f'<i class="fa-solid fa-face-sad-tear" style="color:orange; font-size: 50px;"></i> Negative: {round(score, 3)*100}%'
    else:
        result = f'<i class="fa-solid fa-face-meh" style="color:orange; font-size: 50px;"></i> Neutral: {round(score, 3)*100}%'

    return render_template('examples/sentiment-analysis.html', 
            config=app.config, 
            text_value=text_value, 
            sentiment_result=result)