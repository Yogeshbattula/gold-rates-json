import requests
from bs4 import BeautifulSoup
import json
import datetime
import re

# 1. SETUP URL
url = "https://telugu.goodreturns.in/gold-rates/hyderabad.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print("Fetching data...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# 2. DEFAULT VALUES
gold22 = "₹0"
gold24 = "₹0"
silver = "₹88,000.00" # Default/Fallback

# 3. SCRAPE DATA (Looking for the specific Telugu Text)
# Note: We look for the table cells. This logic is specific to GoodReturns.
tables = soup.find_all('table')

for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        text = row.get_text()
        
        # Logic for 22 Carat (1 Gram)
        if "22 క్యారెట్" in text and "1 గ్రాము" in text:
            cols = row.find_all('td')
            if len(cols) > 1:
                price = cols[1].get_text().strip()
                gold22 = f"₹{price.replace('₹', '').strip()}"

        # Logic for 24 Carat (10 Grams)
        if "24 క్యారెట్" in text and "10 గ్రాముల" in text:
            cols = row.find_all('td')
            if len(cols) > 1:
                price = cols[1].get_text().strip()
                gold24 = f"₹{price.replace('₹', '').strip()}"

# 4. GET TIME
now = datetime.datetime.now()
current_time = now.strftime("%I:%M %p") # e.g., 10:30 AM

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
