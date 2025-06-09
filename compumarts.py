from seleniumbase import SB
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import json
import time

def compumarts_scraper(product_name):
    with SB(test=True, uc=True ,headless=True) as sb:
        sb.open("https://www.compumarts.com/")
        driver = sb.driver
        try:
    #* wait fot the search element and then type the product name for the search
            sb.wait_for_element_present('#header-search')
            sb.type("#header-search", product_name + Keys.ENTER)
    #* wait fot the check box for items in stock then click it 
            sb.wait_for_element_present('.filter__label')
            sb.click('.filter__label')
            sb.wait_for_element_visible('.active-filter')
    #* INFINITE  scroll to the end of the page
            previous_height = driver.execute_script('return document.body.scrollHeight')
            driver.execute_script(f'window.scrollTo(0, 2500)')
            time.sleep(3)
            driver.execute_script(f'window.scrollTo(0, 5000)')
            time.sleep(3)
            while True:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight - 2500)')
                time.sleep(2)
                new_height = driver.execute_script('return document.body.scrollHeight')
                if new_height == previous_height:
                    break
                previous_height = new_height
    #* get the data from the page
            data =[]
            products = sb.find_elements('.card__info-inner')
            for product in products:
                product_link =  product.find_element(By.TAG_NAME,'a').get_attribute('href')
                title =  product.find_element(By.TAG_NAME,'a').text
                price = product.find_element(By.CSS_SELECTOR,'span.price__current').find_element(By.CLASS_NAME,'js-value').text
                data.append({
                        'title': title,
                        'price': price,
                        'link': product_link,
                        'in_stock': True,
                        'store':'compumarts'
                    })
            return data
        except Exception as e:
            print(f'error{e}')
            raise
        