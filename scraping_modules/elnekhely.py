import requests
from bs4 import BeautifulSoup
import logging
import json

logging.basicConfig(level=logging.INFO)

def elnekhely_scraper(product_name):
    logging.info('🔍 scraping elnekhely...')
    
    data = []  # List to store scraped product data
    page_number = 1  # Start from the first page

    while True:
        try:
            # Construct the search URL with product name and current page number
            url = f"https://www.elnekhelytechnology.com/index.php?route=product/search&search={product_name}&page={page_number}"
            r = requests.get(url, timeout=40)
            soup = BeautifulSoup(r.text, 'html.parser')

            # Find all product blocks; stop if none found
            products_container = soup.find('div', class_='main-products')
            if not products_container or not products_container.find_all('div', class_='product-layout'):
                break

            main_products = products_container.find_all('div', class_='product-layout')

            for product in main_products:
                # Extract product title and link
                name_block = product.find('div', class_='name').find('a')
                title = name_block.text
                link = name_block.get('href')

                in_stock = True  # Default to in stock
                price = None

                # Check product label for stock status
                product_label = product.find('div',class_='product-labels')
                if product_label:
                    label_text = product_label.text.strip()
                    if label_text in ['Out Of Stock', 'Coming Soon', 'In Stock']:
                        in_stock = False

                # Get the price from either 'price-normal' or 'price-new'
                price_spans = product.find('div', class_='price').find_all('span')
                for span in price_spans:
                    span_class = span.get('class')[0]
                    if span_class in ['price-normal', 'price-new']:
                        price = span.text

                # Append product data to the result list
                data.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'in_stock': in_stock,
                    'store': 'elnekhely'
                })

            print(f'finished scraping this page {page_number}')
            page_number += 1  # Move to the next page

        except Exception as e:
            logging.error(f'❌ elnekhely scraper failed: {e}')
            break

    logging.info('✅ Finished scraping elnekhely')
    return data
