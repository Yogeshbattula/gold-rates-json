import requests
from bs4 import BeautifulSoup
import json
import datetime

# 1. FETCH DATA (Works with English or Telugu URL)
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
    # Removes '₹', spaces, and 'Rs', but KEEPS commas
    # Input: "₹ 1,43,400" -> Output: "1,43,400"
    return price_str.replace('₹', '').replace('Rs', '').strip()

if soup:
    # --- LOGIC FOR 22 CARAT (1 Gram) ---
    try:
        # Find header with "22"
        header22 = soup.find(lambda tag: tag.name in ['h2', 'h3', 'div'] and "22" in tag.text)
        if header22:
            table = header22.find_next("table")
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if not cols: continue
                
                # Check First Column for specific amount "1"
                # We match strictly "1" to avoid matching "10" or "100"
                amount = cols[0].get_text().strip()
                if amount == "1" or amount == "1 Gram" or amount == "1 గ్రాము":
                    raw_price = cols[1].get_text().strip()
                    gold22 = clean_price(raw_price)
                    print(f"Found 22k (1g): {gold22}")
                    break
    except Exception as e:
        print(f"Error 22k: {e}")

    # --- LOGIC FOR 24 CARAT (10 Grams) ---
    try:
        # Find header with "24"
        header24 = soup.find(lambda tag: tag.name in ['h2', 'h3', 'div'] and "24" in tag.text)
        if header24:
            table = header24.find_next("table")
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if not cols: continue
                
                # Check First Column for specific amount "10"
                amount = cols[0].get_text().strip()
                if amount == "10" or amount == "10 Gram" or amount == "10 గ్రాముల":
                    raw_price = cols[1].get_text().strip()
                    gold24 = clean_price(raw_price)
                    print(f"Found 24k (10g): {gold24}")
                    break
    except Exception as e:
        print(f"Error 24k: {e}")

# 3. TIMESTAMP
now = datetime.datetime.now()
current_time = now.strftime("%I:%M %p") 

# 4. SAVE
data = {
    "gold22": gold22,
    "gold24": gold24,
    "silver": silver,
    "timestamp": current_time
}

print(f"Final Data: {data}")

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
