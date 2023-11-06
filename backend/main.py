from bs4 import BeautifulSoup
import flask
from flask import Flask
from flask import request
import requests
import datetime
import math
import json
import validators
from flask_cors import CORS
import openai


OpenAI_API_Key = "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"
openai.api_key = OpenAI_API_Key


# Returns dictionary
def getNewsAPIResponse(newsTopic, fromDate, toDate):
    newsTopic = requests.utils.quote(newsTopic)
    news_API_Key = "af5b540ddb4248f3a1cc9cf28a5ca332"
    headers = {"X-Api-Key": news_API_Key}
    urlTemplate = "https://newsapi.org/v2/everything?q={newsTopic}&searchIn=description&language=en&from={fromDate}&to={toDate}&pageSize=10&sortBy=relevancy".format(newsTopic=newsTopic, fromDate=fromDate, toDate=toDate)
    response = requests.get(urlTemplate, headers=headers)
    return response.json()

# Returns a list of dictionaries (each dictionary representing an article). Keys are 'source', 'title', 'desc', and 'url'
def getArticles(results):
    articles = []
    if (results['status'] == 'ok'):
        results.pop('status')
        results.pop('totalResults')
        for article in results['articles']:
            newArticle = {}
            newArticle['source'] = article['source']['name']
            newArticle['title'] = article['title']
            newArticle['desc'] = article['description']
            newArticle['url'] = article['url']
            articles.append(newArticle)
    return articles


# Return a dictionary. First keys will be the intervals, ex. '0', '1', '2'... that correspond to a list of articles. Most recent date intervals come first
def searchArticles(newsTopic, intervals, numOfDays, endDate):
    responseData = {}
    for interval in range(intervals):
        startDate = endDate - datetime.timedelta(days=math.floor(numOfDays/intervals))
        response = getNewsAPIResponse(newsTopic, startDate.isoformat(), endDate.isoformat())
        articles = getArticles(response)
        responseData[str(interval)] = articles
        endDate = startDate
    return responseData

# Returns the Title of a given URL as a string
def getNewsHeadline(url):
    if not validators.url(url):
        return ""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0'}
    response = requests.get(url, headers=headers)
    htmlParsed = BeautifulSoup(response.text, features='html.parser')
    return htmlParsed.title.string

# Uses GPT-4 to try to find the topic of the headline
def getTopicFromHeadline(headline):
    prompt = "Give me the general, overarching topic that the following headline is about: \"{headline}\"".format(headline=headline)
    completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", "content": "Your job is to find the overarching topic that a news article could be about given its headline."},{"role": "user", "content": prompt}])
    # content = completion.choices[0].message['content']
    return completion.choices[0].message['content']

app = Flask(__name__)
CORS(app)

# def getHeadlineWrapper(articleURL):
#     return getNewsHeadline(articleURL)

@app.route("/getHeadline/", methods=['GET'])
def getHeadline():
    articleURL = request.headers.get("articleURL")
    articleURL = requests.utils.unquote(articleURL)
    headline = getNewsHeadline(articleURL)
    return headline

@app.route("/getTopic/", methods=['GET'])
def getTopic():
    articleURL = request.headers.get("articleURL")
    articleURL = requests.utils.unquote(articleURL)
    topic = getTopicFromHeadline(getNewsHeadline(articleURL))
    return topic

@app.route("/getResults/", methods=['GET'])
def getResults():
    articleURL = request.headers.get("articleURL")
    articleURL = requests.utils.unquote(articleURL)
    headline = getNewsHeadline(articleURL)
    topic = getTopicFromHeadline(headline)
    endDate = datetime.date.today()
    finalResult = searchArticles(topic, 4, 28, endDate)
    return json.dumps(finalResult)