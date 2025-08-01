from db_product_updater import get_most_searched , add_to_database
from data_collection import merging_data
import logging
logging.basicConfig(level=logging.INFO)





def schedule():
    try :   
        most_searched = get_most_searched()
        for product in most_searched:
            logging.info(f"product name currently begin scraped {product['product_name']}")
            add_to_database(merging_data(product['product_name']))
        logging.info('✅ finished scraping all product')
    
    except Exception as e:
        logging.error(f'thier wasa an error as {e}')
        


if __name__ == "__main__":
    schedule()