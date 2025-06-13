from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import logging


        
def elbadrgroupeg_scraper(product_name):
    try:
        with SB(uc=True, headless=True, headless2=True) as sb:
            logging.info("🔍 Scraping elbadrgroupeg...")
            url = "https://elbadrgroupeg.store/"
            sb.driver.uc_open_with_reconnect(url, 20)  # Increase from 10 to 20 retries
            time.sleep(5)
            
            if sb.is_element_present('.main-content'):
                logging.error('Captcha bypass failed after 20 attempts')
                raise
            else:
                logging.info('Captcha bypassed successfully')

#* wait 5 second then stop the loading of the page and then searsh for the product
            time.sleep(5)
            sb.driver.execute_script("window.stop();")
            try:
                sb.wait_for_element_present('#search-input-el',timeout=15)
                sb.type('#search-input-el',product_name+Keys.ENTER)
            except Exception as e:
                logging.error(f'error {e}')

#* remove any item out of stock
            sb.wait_for_element_present(".filter-checkbox label", timeout=3)
            labels = sb.find_elements(".filter-checkbox label")
            labels[-2].click()
    
    
 #* INFINITE scroll to the end of the page  
            while True:
                sb.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                sb.driver.execute_script('window.scrollBy(0, -60)')
                time.sleep(3)
#* Check if the "no more pages" marker is visible
                if sb.is_element_visible('.ias-noneleft'):
                    break
                try:
#* Find and click all visible .ias-trigger-next buttons
                    next_buttons = sb.find_elements('.ias-trigger-next')
                    for btn in next_buttons:
                        if btn.is_displayed():
                            btn.click()
                            time.sleep(2) 
                except Exception as e:
                    logging.error(f'There was an error: {e}')
#* iniate a data list to append the data collected to it
            data = [] 
#* wait for the caption then extract the data from it
            sb.wait_for_element_present(".caption", timeout=5)
            products = sb.find_elements(".product-layout")
            for product in products:
                try:
                     product.find_element(By.CLASS_NAME,'side-product')
                     break   
                except:
                    title = product.find_element(By.CLASS_NAME, 'name').find_element(By.TAG_NAME, 'a').text
                    product_link = product.find_element(By.CLASS_NAME, 'name').find_element(By.TAG_NAME, 'a').get_attribute('href')
                    price = None
                    spans = product.find_elements(By.TAG_NAME,'span')
                    for span in spans:
                         if span.get_attribute('class') == 'price-normal' or span.get_attribute('class') == 'price-new':
                            price = span.text
                    data.append({
                            'title': title,
                            'price': price,
                            'link': product_link,
                            'in_stock': True,
                            'store':'elbadrgroupeg'
                        })
            logging.info('finshed scrapping elbadrgroupeg')
            return data
    
    except Exception as e:
        logging.warning(f'thier was an error {e}')
        raise