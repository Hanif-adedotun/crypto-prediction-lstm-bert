import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup

def scrape_coindesk(start_date, end_date):
    base_url = "https://www.coindesk.com/search?s=bitcoin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    current_date = start_date
    results = []
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    while current_date <= end_date:
        curr_date_str = current_date.strftime('%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')
        date_unix = int(time.mktime(current_date.timetuple()) * 1000)
        url = f"{base_url}&sd={date_unix}&ed={date_unix}&df=Custom"
        driver.get(url)
    
        # Wait for the search results to load
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "searchstyles__SearchCardWrapper-sc-ci5zlg-21"))
            )
        except:
            print(f"Timeout waiting for search results on {current_date}")
            continue
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        body_content = soup.find('body')
        if body_content:
            print("Body available")
        else:
            print("Body tag not found")
        
        articles = soup.find_all('div', {"class": 'searchstyles__SearchCardWrapper-sc-ci5zlg-21 jjGJEL'}, limit=6)
        print(f"All articles for {current_date}: {len(articles)}")
        for article in articles:
            title_element = article.find('h6', class_='typography__StyledTypography-sc-owin6q-0 dtjHgI')
            title = title_element.text.strip() if title_element else 0
            
            description_element = article.find('p', class_='typography__StyledTypography-sc-owin6q-0')
            description = description_element.text.strip() if description_element else 0
            
            results.append({
                "date": curr_date_str,
                "title": title,
                "description": description
            })
        
        current_date += timedelta(days=1)
    
    return results

# Example usage
start_date = datetime(2019, 1, 1)
end_date = datetime(2024, 9, 30)

scraped_data = scrape_coindesk(start_date, end_date)

# Print the results
# print(json.dumps(scraped_data, indent=2))
print(f"Seccessfully scraped {len(scraped_data)} data from {start_date} to {end_date}")
df = pd.DataFrame(scraped_data)
df.to_csv('./dataset/news-coindesk.csv')