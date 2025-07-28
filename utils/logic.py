import csv

# Platform fee logic
def calculate_profit(price, platform):
    if platform == 'X':
        fee = 0.10 * price
    elif platform == 'Y':
        fee = 0.08 * price + 2
    elif platform == 'Z':
        fee = 0.12 * price
    else:
        return None
    return price - fee  # Profit = Price - Fee

# Condition mapping
condition_mapping = {
    "Like New": {"X": "New", "Y": "3 Stars", "Z": "New"},
    "Good": {"X": "Good", "Y": "2 Stars", "Z": "As New"},
    "Fair": {"X": "Scrap", "Y": "1 Star", "Z": "Good"}
}

# Load inventory
def load_phones():
    phones = []
    with open("data/phones.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['price'] = float(row['price'])
            row['stock'] = int(row['stock'])
            row['sold_directly'] = row['sold_directly'].lower() == 'true'
            phones.append(row)
    return phones

# Check if phone is eligible to be listed
def get_listing_status(phone, platform):
    if phone['stock'] <= 0:
        return False, "Out of Stock"
    if phone['sold_directly']:
        return False, "Sold Directly"
    profit = calculate_profit(phone['price'], platform)
    if profit <= 0:
        return False, "Not Profitable"
    return True, ""
