"""Module to manage the news on the dashboard from updating the articles to displaying the toasts on the right side of the screen.

    Attributes
    ----------
    ARTICLES ( list ):
        A list of articles that is returned from the news api, this is cleared and refreshed everytime a new request is sent to the api.
    removed ( list ):
        A list of articles the user has removed from the dashboard that can later be used to make sure the same articles dont reappear

    Methods
    -------
    news_api_request( covid_terms ):
        Function to get the news data from the news api and return a response in a json format
    get_articles( ):
        A function that returns the list of articles where each entry is a dictionary of title, content pairs.
    update_news( ):
        A function that controls how the articles variable is updated. It requests a new update from the news api and removes any previously removed articles
    remove_from_articles( what_to_remove ):
        A function that removes the articles the user deletes by removing it from the articles list and adding it to the removed list.

"""

import json
import logging
import requests

ARTICLES = []
removed = []

def news_api_request(covid_terms: str="Covid COVID-19 coronavirus") -> json:
    """Function to get the news data from the news api
    
        Parameters:
            covid_terms ( str ):
                The terms used in the news api request to spefify what news articles are returned. By default this has the values, 'Covid COVID-19 coronavirus'
    
        Returns:
            response.json():
                Returns the response from the news api in a json format. ou can access the articles by doing response['articles']
                
    """
    with open("config.json", 'r', encoding='cp1252') as json_data_file:
        data = json.load(json_data_file)
    url = ('https://newsapi.org/v2/everything?'
       'q='+covid_terms+'&'
       'language=en&'
       'sortBy=publishedAt&'
       'apiKey=' + data["api_key"])

    logging.info('Requesting response from news api')
    response = requests.get(url)
    return response.json()

def get_articles() -> list:
    """Function to return the articles list that contains all of the articles from the news api that the users hasnt deleted yet
    
        Returns:
            ARTICLES ( list ):
                A list that contains all of the articles from the news api that the users hasnt deleted yet
    
    """
    return ARTICLES

def update_news(test:str='') -> None:
    """Function to update the news when the user requests or the dashboard refreshes
    
        Parameter:
            test ( str ):
                A variable that exists because one of the tests have it
    """
    global ARTICLES
    response = news_api_request()
    test = response['articles']
    ARTICLES = test
    for article in removed:
        if article in ARTICLES:
            ARTICLES.remove(article)
            logging.info('Article removed from the articles list: ' + article['title'])

def remove_from_articles(what_to_remove:str) -> None:
    """Function to remove an item from the article dictionary
    
        Parameters:
            what_to_remove ( str ):
                The name of the article that is going to be removed from the articles list and added to the removed list
    
    """
    for keys in ARTICLES:
        if keys['title'] == what_to_remove:
            ARTICLES.remove(keys)
            logging.info('Article removed from the articles list: ' + keys['title'])
            removed.append(keys)
            logging.info('Article added to the removed list: ' + keys['title'])
