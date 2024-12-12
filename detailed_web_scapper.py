import requests
import pandas as pd
from pandas import json_normalize

# Define the API URL
api_url = "https://world.openfoodfacts.org/api/v2/search"

# Parameters for the API request
params = {
    "action": "process",
    "json": 1,
    "page_size": 250,  # Maximum allowed products per request
    "countries_tags": "india",  # Only fetch products sold in India
    "page": 1
}

# Function to fetch data from multiple pages
def fetch_data(api_url, params, max_pages=2):
    all_products = []
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        params["page"] = page
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            products = data.get("products", [])
            print(f"Page {page}: Retrieved {len(products)} products.")
            all_products.extend(products)
        else:
            print(f"Error fetching page {page}: {response.status_code}")
            break
    return all_products

# Function to dynamically process and flatten product data
def process_data(products):
    # Use json_normalize to flatten the JSON structure
    df = json_normalize(products, sep="_")
    return df

# Fetch and process data
all_products = fetch_data(api_url, params, max_pages=100)  # Adjust max_pages as needed
df = process_data(all_products)

# Save to an Excel file
output_file = "detailed_food_data_india.xlsx"
df.to_excel(output_file, index=False)
print(f"Data has been saved to '{output_file}'.")


