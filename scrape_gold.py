import requests
from bs4 import BeautifulSoup
import json
import datetime

# 1. FETCH THE ENGLISH PAGE (Same data, easier to code)
url = "https://www.goodreturns.in/gold-rates/hyderabad.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print("Fetching Gold Rates...")
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

if soup:
    # --- LOGIC FOR 22 CARAT (1 Gram) ---
    # We find the Header that says "22 Carat", then grab the table immediately after it.
    try:
        # Find the header (h2, h3, or div)
        header22 = soup.find(lambda tag: tag.name in ['h2', 'h3', 'div'] and "22 Carat" in tag.text)
        if header22:
            table22 = header22.find_next("table")
            # Look for the row starting with "1 gram"
            for row in table22.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) > 1 and "1 gram" in cols[0].text.lower():
                    raw_price = cols[1].text.strip()
                    gold22 = f"₹{raw_price.replace('₹', '').strip()}"
                    break
    except Exception as e:
        print(f"Error finding 22k: {e}")

    # --- LOGIC FOR 24 CARAT (10 Grams - Matching your App UI) ---
    try:
        header24 = soup.find(lambda tag: tag.name in ['h2', 'h3', 'div'] and "24 Carat" in tag.text)
        if header24:
            table24 = header24.find_next("table")
            # Look for the row starting with "10 gram"
            for row in table24.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) > 1 and "10 gram" in cols[0].text.lower():
                    raw_price = cols[1].text.strip()
                    gold24 = f"₹{raw_price.replace('₹', '').strip()}"
                    break
    except Exception as e:
        print(f"Error finding 24k: {e}")

# 3. GET TIME
now = datetime.datetime.now()
current_time = now.strftime("%I:%M %p") 

# 4. SAVE TO JSON
data = {
    "gold22": gold22,
    "gold24": gold24,
    "silver": silver,
    "timestamp": current_time
}

print(f"Final Data: {data}")

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
