from datetime import datetime , date
from db_product_updater import get_most_searched , add_to_database
from data_collection import merging_data
import logging
import json
logging.basicConfig(level=logging.INFO)





def schedule():
    try :
        with open("time.json",'r') as f:
            past_date_str = json.load(f)
        new_date = date.today()
        past_date = datetime.strptime(past_date_str, "%Y-%m-%d").date()
        difference  = (new_date - past_date).days
        
        if difference >= 7:
            
            most_searched = get_most_searched()
            for product in most_searched:
                logging.info(f"product name currently begin scraped {product['product_name']}")
                add_to_database(merging_data(product['product_name']))
            logging.info('✅ finished scraping all product')
            with open("time.json",'w') as f:
                json.dump(str(new_date),f)
        
        else:
            logging.info('wait a week to scrap')
    except Exception as e:
        logging.error(f'thier wasa an error as {e}')
        


if __name__ == "__main__":
    schedule()