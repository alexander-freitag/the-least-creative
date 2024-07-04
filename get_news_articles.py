import json

from bs4 import BeautifulSoup
from newsapi import NewsApiClient
import requests

from keyword_extractor import extract_keywords_ollama
from scripts.handle_articles import save_article, save_raw_article

NEWS_API_KEY = "6cf94ce4aa374f73afc2c4aca4a655e8"
LANGUAGE = 'de'
# Init
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# /v2/top-headlines

# /v2/everything

#TODO: adapt query
response = newsapi.get_everything(q='*',
                                  from_param='2024-06-10',
                                  to='2024-06-28',
                                  language=LANGUAGE,
                                  sort_by='relevancy',
                                  page=10)
if response['status'] == 'ok':
    articles = []
    for article in response['articles']:
        title = article.get('title')
        print("parsing qrticle out of response")
        url = article.get('url')
        published_at = article.get('publishedAt')
        # Lade den vollständigen Artikelinhalt von der URL
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            paragraphs = soup.find_all('p')
            full_content = '\n'.join([para.get_text() for para in paragraphs])
            if len(full_content) < 30 or len(full_content) > 5000:
                continue
            save_article(title, published_at, full_content, LANGUAGE)
            #save_raw_article(title, published_at, full_content, LANGUAGE)
        except Exception as e:
            print(f"Fehler beim Laden des Artikels von {url}: {e}")

    print("Artikel wurden erfolgreich gespeichert.")
else:
    print(f"Fehler bei der Anfrage: {response['status']}")