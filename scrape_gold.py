import requests
from bs4 import BeautifulSoup
import json
import datetime
import re

# 1. FETCH DATA (We use the Telugu URL since your screenshot confirms it loads)
url = "https://telugu.goodreturns.in/gold-rates/hyderabad.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print(f"Fetching data from {url}...")
try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
except Exception as e:
    print(f"Error connecting: {e}")
    soup = None

# 2. DEFAULT VALUES
gold22 = "₹0"
gold24 = "₹0"
silver = "₹88,000.00" 

def clean_price(price_str):
    # Removes "₹", "," and spaces
    return f"₹{price_str.replace('₹', '').replace(',', '').strip()}"

if soup:
    # --- LOGIC FOR 22 CARAT (1 Gram) ---
    try:
        # Search for header containing '22' and ('Carat' or Telugu 'క్యారెట్ల')
        # This regex matches both English and Telugu headers
        header22 = soup.find(lambda tag: tag.name in ['h2', 'h3', 'div'] and "22" in tag.text and ("Carat" in tag.text or "క్యారెట్ల" in tag.text))
        
        if header22:
            print("Found 22k Header")
            # Find the table immediately following the header
            table = header22.find_next("table")
            if table:
                rows = table.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if not cols: continue
                    
                    # We want the row where the first column is "1" (gram)
                    # Text might be "1 gram" or "1 గ్రాము" or just "1"
                    col0_text = cols[0].get_text().strip().lower()
                    if "1" in col0_text and ("g" in col0_text or len(col0_text) < 3):
                        # The Price is usually in the 2nd column (Index 1)
                        raw_price = cols[1].get_text().strip()
                        gold22 = clean_price(raw_price)
                        print(f"Found 22k Price: {gold22}")
                        break
    except Exception as e:
        print(f"Error finding 22k: {e}")

    # --- LOGIC FOR 24 CARAT (10 Grams) ---
    try:
        # Search for header containing '24' and ('Carat' or Telugu 'క్యారెట్ల')
        header24 = soup.find(lambda tag: tag.name in ['h2', 'h3', 'div'] and "24" in tag.text and ("Carat" in tag.text or "క్యారెట్ల" in tag.text))
        
        if header24:
            print("Found 24k Header")
            table = header24.find_next("table")
            if table:
                rows = table.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if not cols: continue
                    
                    # We want the row where first column is "10" (grams)
                    col0_text = cols[0].get_text().strip().lower()
                    if "10" in col0_text:
                        raw_price = cols[1].get_text().strip()
                        gold24 = clean_price(raw_price)
                        print(f"Found 24k Price: {gold24}")
                        break
    except Exception as e:
        print(f"Error finding 24k: {e}")

# 3. TIMESTAMP
now = datetime.datetime.now()
current_time = now.strftime("%I:%M %p") 

# 4. SAVE
data = {
    "gold22": gold22,
    "gold24": gold24, # This will be the 10g price
    "silver": silver,
    "timestamp": current_time
}

print(f"Final Data: {data}")

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
