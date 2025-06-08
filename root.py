from sigma import sigma_scraper
from elnekhely import elnekhelyt_scraper
from elbadrgroupeg import elbadrgroupeg_scraper
import json

#* Get data from different sites and merge them into a single JSON file
def get_data(product_name = None):
    if product_name is None:
        user_input = input("Enter product name (leave blank to skip): ").strip()
        if not user_input:
            print("No product name provided. Skipping data scraping.")
            return
        product_name = user_input

    try:
        # Initialize empty data.json
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump([], f)
            
        # Scrape data from sigma site and load it from data.json
        sigma_scraper(product_name)
        with open("data.json", "r", encoding='utf-8') as f:
            sigma_data = json.load(f)
        
        # Scrape data from elnekhely site and load updated data from data.json
        elnekhelyt_scraper(product_name)
        with open('data.json','r', encoding='utf-8') as f:
            elnekhelyt_data = json.load(f)
        
        # Scrape data from elbadrgroupeg site and load updated data from data.json
        elbadrgroupeg_scraper(product_name)
        with open('data.json','r', encoding='utf-8') as f:
            elbadrgroupeg_data = json.load(f)
    
        # Merge all the scraped data lists
        merged_data = sigma_data + elnekhelyt_data + elbadrgroupeg_data
        
        # Write the merged data back to data.json with pretty formatting
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
            
        
        
    except Exception as e:
        index = 3
        print(f'error : {e} number of retries left {index}')
        while index > 0 :
            get_data(product_name)
            index -=1


if __name__ == "__main__":
    get_data()