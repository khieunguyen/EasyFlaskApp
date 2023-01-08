# -*- coding: utf-8 -*-
from flask import Blueprint

blueprint = Blueprint(
    'example',
    __name__,
    url_prefix='',
    template_folder='../templates',
    static_folder='../static'
)


# Load model here or load model from main app/__init__.py
# poetry add transformers --group dev
from transformers import pipeline

# Load default sentiment analysis from Hugingface Hub
sentiment_pipeline = pipeline("sentiment-analysis") 

# class SentimentAnaliser():
#     def __init__(self):
#         self.sentiment_pipeline = pipeline("sentiment-analysis")
       
#     def analyse(self, text: str):
#         return self.sentiment_pipeline(text)