import requests
import datetime
import math
import json

# Returns dictionary
def getNewsAPIResponse(newsTopic, fromDate, toDate):
    newsTopic = requests.utils.quote(newsTopic)
    apiKey = ""
    headers = {"X-Api-Key":apiKey}
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
        endDate = startDate
        responseData[str(interval)] = articles
    return responseData




finalResult = searchArticles("Israel Palestine", 3, 28, endDate)

print(json.dumps(finalResult, indent=4))