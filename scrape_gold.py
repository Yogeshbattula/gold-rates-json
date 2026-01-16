import requests
from bs4 import BeautifulSoup
import json
import datetime

# 1. USE THE ENGLISH URL (It is more stable for scraping)
url = "https://www.goodreturns.in/gold-rates/hyderabad.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print("Fetching data from English site...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# 2. DEFAULT VALUES
gold22 = "₹0"
gold24 = "₹0"
silver = "₹88,000.00" 

# 3. SCRAPE DATA
# We look for the main gold table by its class
tables = soup.find_all('div', {'class': 'gold_silver_table'})

for div in tables:
    rows = div.find_all('tr')
    for row in rows:
        text = row.get_text().strip()
        
        # Logic for 22 Carat (Standard English Text)
        if "22 Carat" in text and "1 Gram" in text:
            cols = row.find_all('td')
            if len(cols) > 1:
                price = cols[1].get_text().strip()
                # Clean the price: Remove ₹ symbol and spaces
                gold22 = f"₹{price.replace('₹', '').strip()}"

        # Logic for 24 Carat (Standard English Text)
        if "24 Carat" in text and "10 Gram" in text:
            cols = row.find_all('td')
            if len(cols) > 1:
                price = cols[1].get_text().strip()
                gold24 = f"₹{price.replace('₹', '').strip()}"

# 4. GET TIME
now = datetime.datetime.now()
current_time = now.strftime("%I:%M %p") 

# 5. SAVE TO JSON
data = {
    "gold22": gold22,
    "gold24": gold24,
    "silver": silver,
    "timestamp": current_time
}

print(f"Scraped Rates: {data}")

# Write to the file
with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
