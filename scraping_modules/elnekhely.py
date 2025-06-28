from seleniumbase import SB
from selenium.webdriver.common.by import By
import logging
import time
import pprint

def elnekhely_scraper(product_name):
    try:
        with SB(uc=True,headless=True,headless2=True) as sb:
            logging.info('🔍 scraping elnekhely...')
            url = f'https://www.elnekhelytechnology.com/index.php?route=product/search&search={product_name}'
            sb.open(url)
            sb.driver.set_window_size(1920, 1080)

            #* Close cookie notification
            sb.wait_for_element_present('.notification-close', timeout=5)
            sb.click('.notification-close')
            #* Click filter checkbox
            sb.wait_for_element_present('.filter-checkbox')
            sb.click('.filter-checkbox input')
            sb.wait_for_element_absent(".journal-loading-overlay")
            #* Wait for initial product captions
            sb.wait_for_element_visible('.caption', timeout=10)

            #* Infinite scroll until no more results
            sb.driver.set_window_size(1920, 1080)
            while not sb.is_element_present('.ias-noneleft'):
                captions = sb.find_elements(".caption")  # Fresh reference
                if captions:
                    try:
                        sb.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                            captions[-1]
                        )
                        time.sleep(2)  
                    except Exception as e:
                        logging.warning(f"Scrolling issue: {e}")
                        break
                else:
                    break

            #* Final fresh capture of all captions
            captions = sb.find_elements(".caption")
            data = []
            for caption in captions:
                try:
                    price = None
                    a_tag = caption.find_element(By.CLASS_NAME, 'name').find_element(By.TAG_NAME, 'a')
                    title = a_tag.get_attribute('title')
                    product_link = a_tag.get_attribute('href')

                    spans = caption.find_elements(By.TAG_NAME, 'span')
                    for span in spans:
                        if span.get_attribute('class') in ['price-normal', 'price-new']:
                            price = span.text

                    data.append({
                        'title': title,
                        'price': price,
                        'link': product_link,
                        'in_stock': True,
                        'store': 'elnekhely'
                    })
                except Exception as e:
                    logging.warning(f"Failed to parse one caption block: {e}")
                    continue

            logging.info('✅ Finished scraping elnekhely')
            return data

    except Exception as e:
        logging.error(f'❌ elnekhely scraper failed: {e}')
        raise


