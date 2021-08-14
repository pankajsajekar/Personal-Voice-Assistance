import requests

def getgooglenews(no_of_news,region):
    if region == 'india' or region == 'local' or region == 'indian':
        response_news = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=009ea64025bd4295beff6c01e527a17e')
        news_list = []
        for news in range(no_of_news):
            news_list.append(response_news.json().get('articles')[news].get('description'))
        return news_list

    else:
        response_news=requests.get('https://newsapi.org/v2/top-headlines?sources=google-news&apiKey=009ea64025bd4295beff6c01e527a17e')
        news_list = []
        for news in range(no_of_news) :
            news_list.append(response_news.json().get('articles')[news].get('description'))
        return news_list