from seleniumbase import SB
from selenium.webdriver.common.by import By
import time
import logging

def elbadrgroupeg_scraper(product_name):
        with SB(uc=True,headless=True,headless2=True) as sb:
            logging.info("🔍 Scraping elbadrgroupeg...")

            # Construct direct search URL to skip UI interaction
            url = f"https://elbadrgroupeg.store/index.php?route=product/search&search={product_name}"
            
            # Open the page with 20 reconnect retries to bypass Cloudflare challenges
            sb.driver.uc_open_with_reconnect(url, 20)
            time.sleep(5)  # Allow page to settle (initial wait)
            sb.driver.set_window_size(1920, 1080)
            # Check if captcha still appears (i.e., challenge not bypassed)
            if sb.is_element_present('.main-content'):
                logging.error('Captcha bypass failed after 20 attempts')
                raise
            else:
                logging.info('Captcha bypassed successfully')
                
            #* Remove out-of-stock items via filter checkbox interaction
            sb.wait_for_element_present(".filter-checkbox label", timeout=3)
            labels = sb.find_elements(".filter-checkbox label")
            labels[-2].click()  # Click second-to-last label (likely the in-stock filter)
            sb.wait_for_element_absent(".journal-loading-overlay", timeout=10)  # Wait for filtering to finish
    
            #* Initiate a list to store scraped product data
            data = [] 

            #* Wait for products section to load, then capture all product entries
            sb.wait_for_element_present(".main-products", timeout=5)
            products = sb.find_element(".main-products").find_elements(By.CLASS_NAME,'caption')

            #* INFINITE scroll logic — continues until `.ias-noneleft` is visible (end of pagination)
            while not sb.is_element_visible('.ias-noneleft'):
                # Scroll to last loaded product to trigger lazy loading
                sb.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",products[-1])
                
                # Wait for page readiness and confirm new products appear
                sb.wait_for_ready_state_complete()
                sb.wait_for_element_present(".caption", timeout=5)
                products = sb.find_element(".main-products").find_elements(By.CLASS_NAME,'caption')
                
                try:
                    #* Find and click all visible "load more" buttons (pagination)
                    next_buttons = sb.find_elements('.ias-trigger-next')
                    for btn in next_buttons:
                        if btn.is_displayed():
                            btn.click()
                            sb.wait_for_ready_state_complete()
                except Exception as e:
                    logging.error(f'There was an error: {e}')
            
            #* Extract title, price, and link from each product block
            for product in products:  
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

            logging.info('✅finshed scrapping elbadrgroupeg')
            return data

