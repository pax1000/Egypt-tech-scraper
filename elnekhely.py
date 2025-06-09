from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import json
import time

def elnekhelyt_scraper(product_name):
    
    url = 'https://www.elnekhelytechnology.com/'
    
    
    #* Headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    try:
    #* wait for the cookies and click it
        WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CLASS_NAME,'notification-close'))
        )
        cookies_button = driver.find_element(By.CLASS_NAME,'notification-close')
        cookies_button.click()
        search_box = driver.find_element(By.ID,'search-input-el')
        search_box.send_keys(product_name + Keys.ENTER)
        filter_box = driver.find_element(By.CLASS_NAME,'filter-checkbox')
        instock_click = filter_box.find_element(By.TAG_NAME,'input')
        instock_click.click()
    
    
    #* wait until the caption class apear and then extract the data from it
        WebDriverWait(driver,3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,'caption'))
        )
    #* INFINITE  scroll to the end of the page
        previous_height = driver.execute_script('return document.body.scrollHeight')
        data = []
    
    
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == previous_height:
                break
            previous_height = new_height
            
        captions = driver.find_elements(By.CLASS_NAME,'caption')
        try:
            for caption in captions:
    #*     get the title and price from each class and link
                price = None
                title = caption.find_element(By.CLASS_NAME,'name').find_element(By.TAG_NAME,'a').get_attribute('title')
                product_link = caption.find_element(By.CLASS_NAME,'name').find_element(By.TAG_NAME,'a').get_attribute('href')
    #*     the site uses mutible class for price so this check each span for the classes used and then update the price
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
            return data 
            
        except Exception as e:
            print('error:', type(e).__name__, str(e))
            return data  # Return whatever data was collected before the error
            
            
    except Exception as e:
         print('error:', type(e).__name__, str(e))
         raise  
    
    
    finally:
        
        driver.quit()






