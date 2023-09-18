# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 23:30:58 2023

@author: Madhav Appaneni
"""

import requests
from transformers import pipeline


core_name = "NLP"
HOST = "34.125.34.106"
PORT = 8983
solr_url = f"http://{HOST}:{PORT}/solr/{core_name}/query?defType=edismax&"


def parseResponse(response):
    if response.status_code != 200:
        print("Bad URL")
    try:
        data = response.json()["response"]["docs"][0]["fact"]
    except Exception as e:
        print("Exception occured while parsing response, check format:> ", e)
    return data


def fetchFacts(entity):
    req_url = solr_url + 'fl=fact&q.op=OR&q=("' + entity + '")&qf=aliases'
    results = requests.get(req_url)
    return parseResponse(results)


# print(fetchFacts("Chandrababu Naidu"))

summarizer = pipeline(
    "summarization", model="philschmid/bart-large-cnn-samsum", do_sample=True
)


def summarize(text):
    return summarizer(fetchFacts(text))


# print(summarizer(fetchFacts("Chandrababu Naidu")))
