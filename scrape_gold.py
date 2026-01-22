import requests
from bs4 import BeautifulSoup
import json
import datetime

# 1. SETUP
url = "https://telugu.goodreturns.in/gold-rates/hyderabad.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print(f"Fetching data from {url}...")
try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
except Exception as e:
    print(f"Error connecting: {e}")
    soup = None

# Lists to hold all the numbers we find
found_1g_prices = []
found_10g_prices = []

def clean_price_to_int(price_str):
    # Turns "₹ 14,340" into the integer 14340
    clean = price_str.replace('₹', '').replace('Rs', '').replace(',', '').strip()
    if clean.isdigit():
        return int(clean)
    return 0

def format_with_commas(price_int):
    # Turns 14340 back into "14,340"
    return "{:,}".format(price_int)

if soup:
    # Get ALL tables on the page
    tables = soup.find_all("table")
    
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if not cols: continue
            
            # Get the exact text from the first column (e.g., "1" or "10")
            amount_text = cols[0].get_text().strip()
            price_text = cols[1].get_text().strip()
            
            price_val = clean_price_to_int(price_text)
            
            # LOGIC: If column 1 says "1", save the price
            if amount_text == "1" or amount_text == "1 Gram" or amount_text == "1 గ్రాము":
                if price_val > 1000: # Ignore zeroes
                    found_1g_prices.append(price_val)
            
            # LOGIC: If column 1 says "10", save the price
            if amount_text == "10" or amount_text == "10 Gram" or amount_text == "10 గ్రాముల":
                if price_val > 10000:
                    found_10g_prices.append(price_val)

# --- THE MATH ---
# 1. Sort lists from Highest to Lowest
found_1g_prices.sort(reverse=True)   # Example: [14340, 13145]
found_10g_prices.sort(reverse=True)  # Example: [143400, 131450]

gold22_str = "0"
gold24_str = "0"

# 2. Identify 22k vs 24k based on price
# The HIGHER price is always 24k. The LOWER price is 22k.

if len(found_1g_prices) >= 2:
    # We found both tables!
    # 22k is the CHEAPER one (index 1)
    gold22_str = format_with_commas(found_1g_prices[1])
elif len(found_1g_prices) == 1:
    # Only found one table? Assume it's the 22k one just to be safe, or 24k.
    gold22_str = format_with_commas(found_1g_prices[0])

if len(found_10g_prices) >= 1:
    # We want the MOST EXPENSIVE 10g price for the 24k box
    # (Usually 24k is the top table, so index 0 is safe)
    gold24_str = format_with_commas(found_10g_prices[0])

# 3. SAVE
data = {
    "gold22": gold22_str,
    "gold24": gold24_str,
    "silver": "88,000.00",
    "timestamp": datetime.datetime.now().strftime("%I:%M %p")
}

print(f"Debug 1g Found: {found_1g_prices}")
print(f"Debug 10g Found: {found_10g_prices}")
print(f"Saving Data: {data}")

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
