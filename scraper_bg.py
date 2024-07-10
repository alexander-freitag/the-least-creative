# This script is used to scrape the "nova.bg" website and extract the articles from it.
# The articles are saved in a JSON file.
# The script uses the BeautifulSoup library to parse the HTML content of the website.

import requests

from bs4 import BeautifulSoup
from handle_articles import save_article

# Extracts the text, title, and keywords from a "nova.bg" article
def article_nova(url):
    # Make a request to the website using the provided URL
    response = requests.get(url)
    
    # Check if the response is valid
    if response.status_code == 200:
        # Response is valid
        try:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract the title from the h1 tag
            title_tag = soup.find("h1")
            title = title_tag.get_text().strip()

            # Extract the date from the span with class "date-time"
            date_tag = soup.find("span", class_="date-time")
            date = date_tag.get_text().strip()

            # Extract the readable text from #description-wrapper
            description_wrapper = soup.find(id="description-wrapper")
            content = ' '.join(description_wrapper.get_text().split())
    
            return {
                "url": url,
                "title": title,
                "date": date,
                "content": content
            }
        except:
            # Error occurred while parsing the article
            return None
    else:
        # Response is not valid
        return None
    

def save_nova(url):
    article_data = article_nova(url)
    if article_data is not None:
        title = article_data["title"]
        timestamp = article_data["date"]
        content = article_data["content"]
        language = "bg"
        save_article(title, timestamp, content, language)


# Crawl the "nova.bg" website and extract the articles
def crawler_nova(num_pages):
    articles_list = []
    
    # Iterate over the pages
    for page_counter in range(1, num_pages+1):

        # Make a request to the website last news page
        response = requests.get("https://nova.bg/novanews/index/index/" + str(page_counter))
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the news articles div with class "category-list-wrapper"
        div_wrapper = soup.find("div", class_="category-list-wrapper")

        # Find the links to the latest news articles within the div
        links = div_wrapper.find_all("a", class_="title gtm-CategoryListNews-click")
        
        # Iterate over the links and extract the data from each article
        for link in links:
            url = link.get("href")
            article_data = article_nova(url)
            if article_data:
                articles_list.append(article_data)
        
        # Print the progress
        print("Page", page_counter, "done")
    
    return articles_list
