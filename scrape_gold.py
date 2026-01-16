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
    # Removes '₹', 'Rs', and spaces, but KEEPS commas
    return price_str.replace('₹', '').replace('Rs', '').strip()

if soup:
    # --- LOGIC FOR 22 CARAT (1 Gram) ---
    try:
        # We search specifically for the "22" header to get the RIGHT table
        # We look for a header that has "22" inside it
        header22 = soup.find(lambda tag: tag.name in ['h2', 'h3', 'div'] and "22" in tag.text)
        
        if header22:
            # Get the table strictly belonging to this header
            table = header22.find_next("table")
            if table:
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if not cols: continue
                    
                    # Look for "1" in the first column (1 Gram)
                    amount = cols[0].get_text().strip()
                    if amount == "1" or amount == "1 Gram" or amount == "1 గ్రాము":
                        gold22 = clean_price(cols[1].get_text().strip())
                        print(f"Found 22k (1g): {gold22}")
                        break
    except Exception as e:
        print(f"Error 22k: {e}")

    # --- LOGIC FOR 24 CARAT (10 Grams) ---
    try:
        # We search specifically for the "24" header
        header24 = soup.find(lambda tag: tag.name in ['h2', 'h3', 'div'] and "24" in tag.text)
        
        if header24:
            table = header24.find_next("table")
            if table:
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if not cols: continue
                    
                    # Look for "10" in the first column (10 Grams)
                    amount = cols[0].get_text().strip()
                    if amount == "10" or amount == "10 Gram" or amount == "10 గ్రాముల":
                        gold24 = clean_price(cols[1].get_text().strip())
                        print(f"Found 24k (10g): {gold24}")
                        break
    except Exception as e:
        print(f"Error 24k: {e}")

# 3. SAVE TO JSON
data = {
    "gold22": gold22,  # Should be around 13,145
    "gold24": gold24,  # Should be around 1,43,400
    "silver": silver,
    "timestamp": datetime.datetime.now().strftime("%I:%M %p")
}

print(f"Final Data: {data}")

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
