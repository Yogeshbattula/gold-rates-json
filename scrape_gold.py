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

# 2. DEFAULT VALUES
gold22 = "0"
gold24 = "0"
silver = "88,000.00" 

def clean_price(price_str):
    return price_str.replace('₹', '').replace('Rs', '').strip()

if soup:
    # --- STRATEGY: FIND ALL TABLES AND CHECK HEADERS ABOVE THEM ---
    # GoodReturns usually has 24k table first, then 22k table.
    # We will loop through ALL headers to find the right matches.
    
    all_headers = soup.find_all(['h2', 'h3', 'div'])
    
    for header in all_headers:
        text = header.get_text().strip()
        
        # --- LOGIC FOR 24 CARAT (10 Grams) ---
        if "24" in text and ("Carat" in text or "క్యారెట్ల" in text):
            # Found 24k Header -> Look at the table immediately below it
            table = header.find_next("table")
            if table:
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if not cols: continue
                    # We want "10 gram"
                    if "10" in cols[0].get_text() and gold24 == "0":
                        gold24 = clean_price(cols[1].get_text().strip())
                        print(f"Found 24k (10g) in table below '{text}': {gold24}")

        # --- LOGIC FOR 22 CARAT (1 Gram) ---
        if "22" in text and ("Carat" in text or "క్యారెట్ల" in text):
            # Found 22k Header -> Look at the table immediately below it
            table = header.find_next("table")
            if table:
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if not cols: continue
                    # We want "1 gram"
                    # We strictly check for '1' to avoid '10' or '100'
                    amount_text = cols[0].get_text().strip()
                    if (amount_text == "1" or amount_text.startswith("1 ")) and gold22 == "0":
                        gold22 = clean_price(cols[1].get_text().strip())
                        print(f"Found 22k (1g) in table below '{text}': {gold22}")

# 3. SAVE TO JSON
data = {
    "gold22": gold22,  # Target: ~13,145
    "gold24": gold24,  # Target: ~1,43,400
    "silver": silver,
    "timestamp": datetime.datetime.now().strftime("%I:%M %p")
}

print(f"Final Data: {data}")

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
