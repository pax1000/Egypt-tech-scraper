from sigma import sigma_scraper
from elnekhely import elnekhelyt_scraper
from elbadrgroupeg import elbadrgroupeg_scraper
from compumarts import compumarts_scraper
import json
import re

#* Get data from different sites and merge them into a single JSON file
def scrape_with_retry(scraper_function, product_name):
#* get the data from the scraper 
        try:
            data =  scraper_function(product_name)
        except Exception as e:
            print(f'error {e}')
            index = 3
            while index > 0:
                try:
                    data =  scraper_function(product_name)
                    break  # success, exit retry loop
                except Exception as e:
                    index -= 1
                    print(f'number of retries left is {index}, error: {e}')
            else:
#! All retries failed
                data  = []
        return data
#* Merge all the scraped data lists and add them to the data.json file
def merged_data():
 #* the user input the name of the product they want to search or skip to use another method
        product_name = input("Enter product name (leave blank to skip): ").strip()
        if not product_name:
            print("No product name provided. Skipping data scraping.")
            return
#* get the data from each scraper
        sigma_data = scrape_with_retry(sigma_scraper,product_name)
        elnekhelyt_data = scrape_with_retry(elnekhelyt_scraper,product_name)
        elbadrgroupeg_data = scrape_with_retry(elbadrgroupeg_scraper,product_name)
        compumarts_data = scrape_with_retry(compumarts_scraper,product_name)
        merged_data = sigma_data + elnekhelyt_data + elbadrgroupeg_data + compumarts_data
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)

#* load the data to use in diffrent function if needed
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_by_price():
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


#* filter the product by included name like cpu or gpu or motherboard..
def search_products():
    products_name = input('Input product name or part of it like ryzen or intel: ').strip()
    if not products_name:
        print('No product name selected')
        return

    filtered = []
    all_data = load_data()
    for data in all_data:
        words = data['title'].split()
        for word in words:
            if re.search(fr'{products_name}', word, re.IGNORECASE):
                filtered.append(data)
                break
    print(filtered)








#* calling the functions
if __name__ == "__main__":
   merged_data()
   filter_by_price() 
   search_products()