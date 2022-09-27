from covid_news_handling import news_api_request
from covid_news_handling import update_news

def test_news_API_request():
    assert news_api_request()
    assert news_api_request('Covid COVID-19 coronavirus') == news_api_request()

def test_update_news():
    update_news('test')

test_news_API_request()
test_update_news()