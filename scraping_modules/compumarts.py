from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import logging


def compumarts_scraper(product_name):
    logging.info('🔍 scraping compumarts...')
    try:
            with SB(uc=True,headless=True,headless2=True) as sb:
                url = f'https://www.compumarts.com/search?options[prefix]=last&q={product_name}'
                sb.open(url)
                sb.driver.set_window_size(1920, 1080)
#* wait fot the check box for items in stock then click it 
                sb.wait_for_element_present('.filter__label')
                sb.click('.filter__label')
                sb.wait_for_element_visible('.active-filter')
#* INFINITE  scroll to the last product
                sb.wait_for_element_present('.card__info-inner') #wait for the products to appear
                products = sb.find_elements('.card__info-inner') #find all the products and make a list of them
                previous_length = 0 
                current_length = len(products)
                while previous_length != current_length: #use a loop to scroll untill the last product
                    previous_length = len(products)
                    sb.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",products[-1])
                    time.sleep(5) #time for the products to load
                    products = sb.find_elements('.card__info-inner') #updating the products to the last elements
                    current_length = len(products)
#* get the data from the page
                data =[]
                for product in products: # iteration the products and extract the element from them
                    product_link =  product.find_element(By.TAG_NAME,'a').get_attribute('href') # get the product link from the href
                    title =  product.find_element(By.TAG_NAME,'a').text # get the title of the product
                    price = product.find_element(By.CSS_SELECTOR,'span.price__current').find_element(By.CLASS_NAME,'js-value').text #get the price 
                    data.append({
                            'title': title,
                            'price': price,
                            'link': product_link,
                            'in_stock': True,
                            'store':'compumarts'
                        })
                logging.info('✅finshed scrapping compumarts')
                return data      # return the collected data
    except Exception as e:
            logging.error(f'❌ compumarts scraper failed: {e}')
            raise