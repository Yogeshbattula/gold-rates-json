import requests
import json
import datetime
import re

# 1. SETUP (Try English URL first, it's usually cleaner)
url = "https://www.goodreturns.in/gold-rates/hyderabad.html"
# We act like a real Chrome browser to avoid being blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

print(f"Fetching {url}...")
try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}") # Should be 200
    text = response.text
except Exception as e:
    print(f"Error fetching page: {e}")
    text = ""

# 2. FIND ALL NUMBERS (REGEX)
# This looks for any number pattern like "14,340" or "1,43,400"
# It ignores all HTML tags.
matches = re.findall(r'₹?[\s]*([0-9]{1,3}(?:,[0-9]{2,3})+)', text)

# Convert all matches to pure integers (e.g., 14340)
found_prices = []
for m in matches:
    try:
        val = int(m.replace(',', '').strip())
        found_prices.append(val)
    except:
        continue

# Sort from Highest to Lowest
found_prices = sorted(list(set(found_prices)), reverse=True)
print(f"All Numbers Found: {found_prices}")

# 3. MATH LOGIC (The Smart Part)
gold22 = "0"
gold24 = "0"
silver = "88,000.00"

# LOGIC FOR 10 GRAMS (24k vs 22k)
# Prices for 10g are usually between 1,00,000 and 2,00,000
prices_10g = [p for p in found_prices if 100000 < p < 200000]

if len(prices_10g) >= 2:
    gold24 = "{:,}".format(prices_10g[0]) # Highest is 24k (e.g. 1,56,000)
elif len(prices_10g) == 1:
    gold24 = "{:,}".format(prices_10g[0])

# LOGIC FOR 1 GRAM (22k)
# Prices for 1g are usually between 10,000 and 20,000
prices_1g = [p for p in found_prices if 10000 < p < 20000]

if len(prices_1g) >= 2:
    # If we find two 1g prices, the LOWER one is usually 22k (e.g. 14,300 vs 15,600)
    # We explicitly look for the smaller one
    gold22 = "{:,}".format(prices_1g[-1]) 
elif len(prices_1g) == 1:
    gold22 = "{:,}".format(prices_1g[0])

# 4. SAVE DATA
data = {
    "gold22": gold22,
    "gold24": gold24,
    "silver": silver,
    "timestamp": datetime.datetime.now().strftime("%I:%M %p")
}

print(f"FINAL SAVED DATA: {data}")

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
