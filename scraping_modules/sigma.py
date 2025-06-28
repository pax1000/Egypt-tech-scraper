from seleniumbase import SB
from selenium.webdriver.common.by import By
import logging
import time
def sigma_scraper(product_name): 
    logging.info('🔍 scraping sigma...')
    try:
        with SB (uc=True,headless=True,headless2=True) as sb:
            url = f"https://www.sigma-computer.com/search?search={product_name}&submit_search=&route=product%2Fsearch"
            sb.driver.uc_open_with_reconnect(url, 20)
            sb.driver.set_window_size(1920, 1080)
            time.sleep(5)  # Allow page to settle (initial wait)
            # Check if captcha still appears (i.e., challenge not bypassed)
            if sb.is_element_present('.main-content'):
                logging.error('Captcha bypass failed after 20 attempts')
                raise
            else:
                logging.info('Captcha bypassed successfully')

#* Wait for products to load
            sb.wait_for_element_present('.right-block', timeout=20)
#* get the items from the page then iterate over it to extract the data
            items = sb.find_elements('.right-block')
#* the data to be returned
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
            data = [item for item in data if item['in_stock']]
            logging.info('✅finshed scrapping sigma')
            return data
    except Exception as e:
        logging.error(f'❌ Sigma scraper failed: {e}')
        raise

