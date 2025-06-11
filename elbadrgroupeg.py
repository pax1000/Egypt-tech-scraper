from seleniumbase import SB
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

def elbadrgroupeg_scraper(product_name):
    def try_captcha_bypass(sb):
        if sb.is_element_visible('#search-input-el'):
            print("Search bar is visible. CAPTCHA likely bypassed.")
            return

        if (
            sb.is_element_visible('iframe[src*="challenge"]') or 
            sb.is_element_visible('iframe[src*="turnstile"]') or
            'captcha' in sb.get_page_source().lower()
        ):
            print("CAPTCHA challenge detected. Attempting bypass...")
            sb.uc_gui_click_captcha()
        else:
            print("No CAPTCHA or search bar found. Skipping interaction.")

    # --- MAIN SCRIPT ---
    with SB(uc=True ,headless=True) as sb:
        sb.uc_open_with_reconnect("https://elbadrgroupeg.store/", 3)

        try_captcha_bypass(sb)

        # ✅ Check if bypass was successful
        if not sb.is_element_visible('#search-input-el'):
            raise Exception("❌ Still blocked — challenge likely failed.")
        
        print("✅ Human check passed. Proceeding...")
        time.sleep(5)
        sb.driver.execute_script("window.stop();")

        try:
            # Wait for the search input, then type and search
            sb.wait_for_element_present("#search-input-el", timeout=10)
            sb.type("#search-input-el", product_name + Keys.ENTER)
            time.sleep(5)
            sb.driver.execute_script("window.stop();")

            # Remove items out of stock
            sb.wait_for_element_present(".filter-checkbox label", timeout=3)
            labels = sb.find_elements(".filter-checkbox label")
            labels[-2].click()  

            data = []  # Data store

            # Infinite scroll to load all items
            while True:
                sb.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                sb.driver.execute_script('window.scrollBy(0, -60)')
                time.sleep(3)

                if sb.is_element_visible('.ias-noneleft'):
                    break

                try:
                    next_buttons = sb.find_elements('.ias-trigger-next')
                    for btn in next_buttons:
                        if btn.is_displayed():
                            btn.click()
                            time.sleep(2)
                except Exception as e:
                    print(f'There was an error: {e}')

            # Extract product data
            sb.wait_for_element_present(".caption", timeout=5)
            products = sb.find_elements(".product-layout")

            for product in products:
                try:
                    # Skip side-product blocks
                    product.find_element(By.CLASS_NAME, 'side-product')
                    continue
                except:
                    title = product.find_element(By.CLASS_NAME, 'name').find_element(By.TAG_NAME, 'a').text
                    product_link = product.find_element(By.CLASS_NAME, 'name').find_element(By.TAG_NAME, 'a').get_attribute('href')
                    price = None
                    spans = product.find_elements(By.TAG_NAME, 'span')
                    for span in spans:
                        cls = span.get_attribute('class')
                        if cls == 'price-normal' or cls == 'price-new':
                            price = span.text
                    data.append({
                        'title': title,
                        'price': price,
                        'link': product_link,
                        'in_stock': True,
                        'store': 'elbadrgroupeg'
                    })

            return data

        except Exception as e:
            print(f'There was an error: {e}')
            raise
