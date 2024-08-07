import json
import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from dataset import save_article

NEWS_API_KEY = "906dfbcb405b487d8e61393e5fe929de"
LANGUAGE = 'de'
newsapi = NewsApiClient(api_key=NEWS_API_KEY)
response = newsapi.get_everything(q='*',
                                  from_param='2024-06-28',
                                  to='2024-07-02',
                                  language=LANGUAGE,
                                  sort_by='relevancy',
                                  page=5)
if response['status'] == 'ok':
    articles = []
    for article in response['articles']:
        title = article.get('title')
        print("parsing article out of response")
        url = article.get('url')
        published_at = article.get('publishedAt')
        # Load the full article content from the URL
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            paragraphs = soup.find_all('p')
            full_content = '\n'.join([para.get_text() for para in paragraphs])
            if len(full_content) < 50 or len(full_content) > 10000:
                continue
            save_article(title, published_at, full_content, LANGUAGE)
        except Exception as e:
            print(f"Error loading article from {url}: {e}")

    print("Articles saved successfully.")
else:
    print(f"Request error: {response['status']}")