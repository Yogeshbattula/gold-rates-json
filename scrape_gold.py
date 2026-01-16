import requests
from bs4 import BeautifulSoup
import json
import datetime

# 1. FETCH DATA
url = "https://telugu.goodreturns.in/gold-rates/hyderabad.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print(f"Fetching data from {url}...")
try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
except Exception as e:
    print(f"Error connecting: {e}")
    soup = None

# 2. LISTS TO STORE FOUND PRICES
prices_1g = []
prices_10g = []

def clean_price_to_int(price_str):
    # Turns "₹ 14,340" into the number 14340 for math comparison
    clean = price_str.replace('₹', '').replace('Rs', '').replace(',', '').strip()
    return int(clean) if clean.isdigit() else 0

def format_price(price_int):
    # Turns 14340 back into "14,340"
    return "{:,}".format(price_int)

if soup:
    # FIND ALL TABLES ON THE PAGE
    tables = soup.find_all("table")
    
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if not cols: continue
            
            amount = cols[0].get_text().strip()
            price_text = cols[1].get_text().strip()
            
            # Check for "1 Gram" Rows
            if amount == "1" or amount == "1 Gram" or amount == "1 గ్రాము":
                p_val = clean_price_to_int(price_text)
                if p_val > 1000: # Filter out weird small numbers
                    prices_1g.append(p_val)
            
            # Check for "10 Gram" Rows
            if amount == "10" or amount == "10 Gram" or amount == "10 గ్రాముల":
                p_val = clean_price_to_int(price_text)
                if p_val > 10000:
                    prices_10g.append(p_val)

# 3. APPLY MATH LOGIC
# Sort the lists. Highest is 24k, Lowest (but valid) is 22k.
prices_1g.sort(reverse=True)   # [14340, 13145]
prices_10g.sort(reverse=True)  # [143400, 131450]

# Default values if scraping fails
gold22_val = 0
gold24_val = 0

if len(prices_1g) >= 2:
    gold24_val_1g = prices_1g[0] # Highest (Expensive)
    gold22_val = prices_1g[1]    # Second Highest (Cheaper)
elif len(prices_1g) == 1:
    gold24_val_1g = prices_1g[0] # Assume only found 24k

if len(prices_10g) >= 1:
    gold24_val = prices_10g[0]   # We want 10g for the 24k box

# 4. FINAL FORMATTING (Add commas back)
gold22_str = format_price(gold22_val)      # e.g. "13,145"
gold24_str = format_price(gold24_val)      # e.g. "1,43,400"
silver = "88,000.00"

# 5. SAVE
data = {
    "gold22": gold22_str,
    "gold24": gold24_str,
    "silver": silver,
    "timestamp": datetime.datetime.now().strftime("%I:%M %p")
}

print(f"Found Prices (1g): {prices_1g}")
print(f"Found Prices (10g): {prices_10g}")
print(f"Final Data: {data}")

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
