from seleniumbase import SB
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import json
import time

def elbadrgroupeg_scraper(product_name):

    with SB(test=True, uc=True, headless=True) as sb:
        sb.open("https://elbadrgroupeg.store/")
        
        time.sleep(5)
        sb.driver.execute_script("window.stop();")
        
        try :
            #* wait for the search element presence and then search    
                sb.wait_for_element_present("#search-input-el", timeout=10)
                sb.type("#search-input-el", product_name + Keys.ENTER)
                time.sleep(5)
                sb.driver.execute_script("window.stop();")
            
            
            #* remove any item out of stock
                sb.wait_for_element_present(".filter-checkbox label", timeout=3)
                labels = sb.find_elements(".filter-checkbox label")
                labels[-2].click() 
                
    #* the data that will be appended and then send to the json
                data = [] 
            
            #* INFINITE scroll to the end of the page             
                previous_height = sb.driver.execute_script('return document.body.scrollHeight')
                                              
                
                while True:
                    sb.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    sb.driver.execute_script('window.scrollBy(0, -60)')
                    time.sleep(3)
            
                # Check if the "no more pages" marker is visible
                    if sb.is_element_visible('.ias-noneleft'):
                        break
            
                    try:
                        # Find and click all visible .ias-trigger-next buttons
                        next_buttons = sb.find_elements('.ias-trigger-next')
                        for btn in next_buttons:
                            if btn.is_displayed():
                                btn.click()
                                time.sleep(2)  # small delay after click
                
                    except Exception as e:
                        print(f'There was an error: {e}')
                    
            
            
            
            # #* wait for the caption then extract the data from it
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
                
        except Exception as e:
             print(f'There was an error: {e}')
        
            #* write JSON after all data is collected
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)