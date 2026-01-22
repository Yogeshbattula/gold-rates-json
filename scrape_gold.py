import requests
import json
import datetime
import re

# 1. FETCH THE PAGE CONTENT (Text only)
url = "https://telugu.goodreturns.in/gold-rates/hyderabad.html"
headers = {'User-Agent': 'Mozilla/5.0'}
print(f"Fetching {url}...")

try:
    response = requests.get(url, headers=headers)
    text = response.text
except Exception as e:
    print(f"Error: {e}")
    text = ""

# 2. FIND PRICES USING PATTERN MATCHING (REGEX)
# We look for patterns like "13,145" or "1,43,400"
# This ignores HTML tags completely.

# Find all numbers that look like prices (digits with commas)
matches = re.findall(r'₹?[\s]*([0-9]{1,3}(?:,[0-9]{2,3})+)', text)

print(f"All patterns found: {matches}")

gold22 = "0"
gold24 = "0"
silver = "88,000.00"

found_prices = []

# Convert matches to integers to find the right ones
for price_str in matches:
    try:
        # Remove commas to check value
        val = int(price_str.replace(',', '').strip())
        found_prices.append(val)
    except:
        continue

# Sort numbers: High to Low
found_prices.sort(reverse=True)
print(f"Sorted Valid Prices: {found_prices}")

# LOGIC:
# The prices on the page are usually:
# ~1,43,000 (24k 10g)
# ~1,31,000 (22k 10g)
# ~14,300   (24k 1g)
# ~13,100   (22k 1g)

# We want 24k (10g) -> Highest value > 100,000
for p in found_prices:
    if p > 100000:
        gold24 = "{:,}".format(p) # Format back to 1,43,400
        break

# We want 22k (1g) -> Value around 13,000 (but less than 24k 1g)
# We look for a price between 10,000 and 20,000
possible_1g = [p for p in found_prices if 10000 < p < 20000]

if len(possible_1g) >= 2:
    # If we find 14k and 13k, the SMALLER one is 22k
    gold22 = "{:,}".format(possible_1g[1]) # The second highest is 22k
elif len(possible_1g) == 1:
    # If we only find one, it's risky, but assume it's the rate
    gold22 = "{:,}".format(possible_1g[0])

# 3. SAVE TO JSON
data = {
    "gold22": gold22,
    "gold24": gold24,
    "silver": silver,
    "timestamp": datetime.datetime.now().strftime("%I:%M %p")
}

print(f"FINAL SAVED DATA: {data}")

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
