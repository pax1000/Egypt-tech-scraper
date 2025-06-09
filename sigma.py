from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

def sigma_scraper(product_name):
    url = "https://www.sigma-computer.com/home"
    
    
    #* Headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    try:
        search_box = driver.find_element(By.CLASS_NAME, "autosearch-input")
        search_box.send_keys(product_name + Keys.ENTER)
    
        # Wait for products to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-layout'))
        )
    
        items = driver.find_elements(By.CLASS_NAME, 'right-block')
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
                print(f"Error parsing item: {e}")
    
        return data
    
    except TimeoutException:
        print("Timeout: Products did not load in time.")
        raise
    finally:
        driver.quit()
   
