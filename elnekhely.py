from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging

def elnekhelyt_scraper(product_name):
        try:
            with SB(uc=True,headless=True,headless2=True) as sb:
                logging.info('🔍 scraping elnekhelyt...')
                url = 'https://www.elnekhelytechnology.com/'
                sb.open(url)
#* wait for the coockies to appear then click it
                sb.wait_for_element_present('.notification-close',timeout=5)
                sb.click('.notification-close')
#* wait for the searchbar to appear and then click it 
                sb.wait_for_element_present('#search-input-el')
                sb.type('#search-input-el',product_name+Keys.ENTER)
#* wait for the filter by stock option to appear and then click it
                sb.wait_for_element_present('.filter-checkbox',timeout=10)
                sb.click('.filter-checkbox input')
#* wait fo the caption element to appear 
                sb.wait_for_element_visible('.caption',timeout=10)
                captions = sb.find_elements(".caption")
#* scroll to the last element with the class caption until the elment with .ias-noneleft appear 
                while not sb.is_element_present('.ias-noneleft'):
                    sb.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    captions[-1])
                    captions = sb.find_elements(".caption")
                data = []
                for caption in captions:
#* get the title and price from each class and link
                        price = None
                        title = caption.find_element(By.CLASS_NAME,'name').find_element(By.TAG_NAME,'a').get_attribute('title')
                        product_link = caption.find_element(By.CLASS_NAME,'name').find_element(By.TAG_NAME,'a').get_attribute('href')
#* the site uses mutible class for price so this check each span for the classes used and then update the price
                        spans = caption.find_elements(By.TAG_NAME,'span')
                        for span in spans:
                            if span.get_attribute('class') == 'price-normal' or span.get_attribute('class') == 'price-new':
                                price = span.text
#* append data to the data list
                        data.append({
                            'title': title,
                            'price': price,
                            'link': product_link,
                            'in_stock': True,
                            'store':'elnekhely'
                        })
                logging.info('finshed scrapping elnekhely')
                return data
                
        except Exception as e :
            logging.error(f'❌ elnekhely scraper failed: {e}')
            raise