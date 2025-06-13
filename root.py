from sigma import sigma_scraper
from elnekhely import elnekhelyt_scraper
from elbadrgroupeg import elbadrgroupeg_scraper
from compumarts import compumarts_scraper
import json
import re
from concurrent.futures import ThreadPoolExecutor
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('seleniumbase').setLevel(logging.ERROR)
logging.getLogger('seleniumbase.core.browser_launcher').setLevel(logging.ERROR)
logging.getLogger('seleniumbase.plugins.pytest_plugin').setLevel(logging.ERROR)

#* Get data from different sites and merge them into a single JSON file
def scrape_with_retry(scraper_function, product_name):
    try:
        data = scraper_function(product_name)
        if not isinstance(data, list):  # Ensure it's a list
            data = []
    except Exception as e:
        print(f'Initial attempt failed: {e}')
        index = 3
        while index > 0:
            print(f"Retrying... attempts left: {index} name of the scraper {scraper_function}")
            try:
                data = scraper_function(product_name)
                if not isinstance(data, list):
                    data = []
                break
            except Exception as e:
                index -= 1
                print(f'number of retries left is {index}, error: {e}')
        else:
            data = []  # All retries failed
    return data
#* Merge all the scraped data lists and add them to the data.json file
def merged_data():
 #* the user input the name of the product they want to search or skip to use another method
        product_name = input("Enter product name (leave blank to skip): ").strip()
        if not product_name:
            print("No product name provided. Skipping data scraping.")
            return
#* get the data from each scraper
        with ThreadPoolExecutor() as executor:
            # Submit scraper tasks
            future_sigma = executor.submit(scrape_with_retry, sigma_scraper, product_name)
            future_elnekhelyt = executor.submit(scrape_with_retry, elnekhelyt_scraper, product_name)
            future_elbadrgroupeg = executor.submit(scrape_with_retry, elbadrgroupeg_scraper, product_name)
            future_compumarts = executor.submit(scrape_with_retry, compumarts_scraper, product_name)
    
            # Wait for all results
            sigma_data = future_sigma.result()
            elnekhelyt_data = future_elnekhelyt.result()
            elbadrgroupeg_data = future_elbadrgroupeg.result()
            compumarts_data = future_compumarts.result()
            merged_data = sigma_data + elnekhelyt_data + elbadrgroupeg_data + compumarts_data
            
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)

#* load the data to use in diffrent function if needed
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def filter_by_price(data):
    data = load_data()
    # Get min and max price from user
    min_price = input("Input minimum price to filter: ")
    max_price = input("Input maximum price to filter: ")
    # Convert or default
    min_price = int(min_price) if min_price.isdigit() else 0
    max_price = int(max_price) if max_price.isdigit() else float('inf')
# the filter data
    filtered = []
# loop for the data and get the items in the max to min range
    for item in data:
        price_str = item.get('price', '')
        price = int(''.join(re.findall(r'[0-9]', price_str))) if price_str else 0
        if min_price <= price <= max_price:
            filtered.append(item)
    return filtered

#* filter the product by included name like cpu or gpu or motherboard..
def filter_by_name(data):
    products_name = input('Input product name or part of it like ryzen or intel: ').strip()
    if not products_name:
        print('No product name selected')
        return data
    filtered = []
    for item in data:
        words = item['title'].split()
        for word in words:
            if re.search(fr'{products_name}', word, re.IGNORECASE):
                filtered.append(item)
                break
    return filtered
#* filter by avilabilty

def filter_by_stock(data):
    filtered = []
    for item in data:
        if item['in_stock']:
            filtered.append(item)
    return filtered



def main_processing():
    merged_data()
    data = load_data()
    data = filter_by_price(data)
    data = filter_by_name(data)
    data = filter_by_stock(data)
    with open('filtered.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)






#* calling the functions
if __name__ == "__main__":
   main_processing()