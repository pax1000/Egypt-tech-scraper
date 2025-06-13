from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging

def sigma_scraper(product_name): 
    logging.info('🔍 scraping sigma...')
    try:
        with SB (uc=True,headless=True,headless2=True) as sb:
            url = "https://www.sigma-computer.com/home"
            sb.open(url)
#* wait for the search files to be visible and then search the products
            sb.wait_for_element_visible('.autosearch-input')
            sb.type('.autosearch-input',product_name+Keys.ENTER)
#* Wait for products to load
            sb.wait_for_element_present('.right-block', timeout=20)
#* get the items from the page then iterate over it to extract the data
            items = sb.find_elements('.right-block')
            data = []
            for item in items:
                try:
                    link_element = item.find_element(By.TAG_NAME, 'a')
                    title = link_element.get_attribute('title')
                    price = item.find_element(By.CLASS_NAME, 'price-new').text
                    product_link = link_element.get_attribute('href')
                    in_stock = None
                    spans = item.find_elements(By.TAG_NAME, 'span')
                    for span in spans:
                        text = span.text.strip().lower()
                        if text == 'in stock':
                            in_stock = True
                            break
                        elif text == 'out of stock':
                            in_stock = False
                            break
        
                    data.append({
                        'title': title,
                        'price': price,
                        'link': product_link,
                        'in_stock': in_stock,
                        'store':'sigma'
                    })
            
                except Exception as e:
                    logging.error(f"Error parsing item: {e}")
                    return data
            logging.info('finshed scrapping sigma')
            return data
    except Exception as e:
        logging.error(f'❌ Sigma scraper failed: {e}')
        raise