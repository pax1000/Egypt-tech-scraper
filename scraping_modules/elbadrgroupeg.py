import requests
from bs4 import BeautifulSoup
import logging

def elbadrgroupeg_scraper(product_name):
    logging.info('🔍 scraping elbadrgroupeg...')  # Log the start of the scraping process

    data = []  # List to store product info
    page_number = 1  # Start from the first page

    while True:
        try:
            # Construct the search URL with the product name and current page
            url = f"https://elbadrgroupeg.store/index.php?route=product/search&search={product_name}&page={page_number}"
            r = requests.get(url, timeout=40)
            soup = BeautifulSoup(r.text, 'html.parser')

            # Find all product blocks; stop the loop if none found
            products_container = soup.find('div', class_='main-products')
            if not products_container or not products_container.find_all('div', class_='product-layout'):
                break

            main_products = products_container.find_all('div', class_='product-layout')

            for product in main_products:
                # Extract the product title and link
                name_block = product.find('div', class_='name').find('a')
                title = name_block.text
                link = name_block.get('href')

                in_stock = True  # Assume product is in stock
                price = None  # Initialize price

                # Check for "Out Of Stock" or "Coming Soon" labels
                product_label = product.find('span', class_='product-label')
                if product_label:
                    label_text = product_label.text.strip()
                    if label_text in ['Out Of Stock', 'Coming Soon']:
                        in_stock = False

                # Find and extract the price
                price_spans = product.find('div', class_='price').find_all('span')
                for span in price_spans:
                    span_class = span.get('class')[0]
                    if span_class in ['price-normal', 'price-new']:
                        price = span.text

                # Add the product data to the list
                data.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'in_stock': in_stock,
                    'store': 'elbadrgroupeg'
                })

            print(f'finished scraping this page {page_number}')
            page_number += 1  # Move to next page

        except Exception as e:
            print(f'there was an error as {e}')  # Print the error
            break

    logging.info('✅finshed scrapping elbadrgroupeg')  # Log completion
    return data


