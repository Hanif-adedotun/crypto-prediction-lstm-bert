import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import time
import random

def get_article_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = soup.find_all('article', class_='story')
    data = []
    
    for article in articles[:5]:  # Limit to 5 articles per day
        title = article.find('h3').text.strip()
        description = article.find('p', class_='story__excerpt').text.strip()
        date = article.find('time')['datetime']
        
        data.append({
            'title': title,
            'description': description,
            'date': date
        })
    
    return data

def scrape_bitcoin_news(start_date, end_date):
    all_data = []
    current_date = start_date
    
    while current_date <= end_date:
        formatted_date = current_date.strftime("%Y/%m/%d")
        url = f"https://news.bitcoin.com/{formatted_date}/"
        
        print(f"Scraping articles for {formatted_date}")
        articles = get_article_data(url)
        
        for article in articles:
            all_data.append([article['date'], article['title'], article['description']])
        
        current_date += timedelta(days=1)
        time.sleep(random.uniform(1, 3))  # Random delay between requests
    
    return all_data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Title', 'Description'])
        writer.writerows(data)

if __name__ == "__main__":
    start_date = datetime(2019, 1, 1)
    end_date = datetime.now()
    
    news_data = scrape_bitcoin_news(start_date, end_date)
    save_to_csv(news_data, 'bitcoin_news.csv')
    
    print(f"Scraping complete. Data saved to bitcoin_news.csv")