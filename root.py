from sigma import sigma_scraper
from elnekhely import elnekhelyt_scraper
from elbadrgroupeg import elbadrgroupeg_scraper
from compumarts import compumarts_scraper
import json
import re

#* Get data from different sites and merge them into a single JSON file
def get_data(product_name = None):
    if product_name is None:
        user_input = input("Enter product name (leave blank to skip): ").strip()
        if not user_input:
            print("No product name provided. Skipping data scraping.")
            return
        product_name = user_input
    try:
#* try sigma scrpaer then break and return the data if it break three times
        try:
            sigma_data =  sigma_scraper(product_name)
        except Exception as e:
            print(f'error {e}')
            index = 3
            while index > 0:
                try:
                    sigma_data =  sigma_scraper(product_name)
                    break  # success, exit retry loop
                except Exception as e:
                    index -= 1
                    print(f'number of retries left is {index}, error: {e}')
            else:
                # All retries failed
                sigma_data = []
#* try elnekhelyt scrpaer then break and return the data if it break three times
        try:
           elnekhelyt_data = elnekhelyt_scraper(product_name)
        except Exception as e:
            print(f'error {e}')
            index = 3
            while index > 0:
                try:
                    elnekhelyt_data = elnekhelyt_scraper(product_name)
                    break  # success, exit retry loop
                except Exception as e:
                    index -= 1
                    print(f'number of retries left is {index}, error: {e}')
            else:
                # All retries failed
                elnekhelyt_data = []

#* try elbadrgroupeg scrpaer then break and return the data if it break three times

        try:
            elbadrgroupeg_data = elbadrgroupeg_scraper(product_name)
        except Exception as e:
            print(f'error {e}')
            index = 3
            while index > 0:
                try:
                    elbadrgroupeg_data = elbadrgroupeg_scraper(product_name)
                    break  # success, exit retry loop
                except Exception as e:
                    index -= 1
                    print(f'number of retries left is {index}, error: {e}')
            else:
                # All retries failed
                elbadrgroupeg_data = []

#* try compumarts scrpaer then break and return the data if it break three times
        try:
            compumarts_data = compumarts_scraper(product_name)
        except Exception as e:
            print(f'error {e}')
            index = 3
            while index > 0:
                try:
                    compumarts_data = compumarts_scraper(product_name)
                    break  # success, exit retry loop
                except Exception as e:
                    index -= 1
                    print(f'number of retries left is {index}, error: {e}')
            else:
                # All retries failed
                compumarts_data = []
#* Merge all the scraped data lists and add them to the data.json file
        merged_data = sigma_data + elnekhelyt_data + elbadrgroupeg_data + compumarts_data
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
            

        
    except Exception as e:
        print(f'error : {e}')
    

# #* filter  the products by price
# def filter_by_price(min_price = None,max_price =None):
#     min_price = input("input minmum price to filter :")
#     max_price = input('input maximum price to filter :')
#     filtered = []
#     with open('data.json','r', encoding='utf-8') as f:
#             all_data = json.load(f)
#             for data in all_data:
#                 price =  (int(''.join(re.findall("[0-9]",data['price']))))
#                 if price > int(min_price) and price < int(max_price):
#                     filtered.append(data)

#     print(filtered)
                

    







#* calling the functions
if __name__ == "__main__":
    get_data()

