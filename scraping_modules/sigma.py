import requests
from bs4 import BeautifulSoup
import logging

def sigma_scraper(product_name): 
    logging.info('🔍 scraping sigma...')

    try:     
        # Construct search URL with query
        url = f'https://www.sigma-computer.com/search?search={product_name}&submit_search=&route=product%2Fsearch'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Find all product containers on the page
        products_layout = soup.find_all('div', class_='product-item-container')
        
        data = []  # Store product data

        for product in products_layout:
            # Extract title and product link
            title = product.find('a').get('title')   
            link = 'https://www.sigma-computer.com/' + product.find('a').get('href') 

            # Extract new price (assumes it's always present)
            price = product.find('span', class_='price-new').text 

            # Check stock status by looking through all span tags
            in_stock = None
            spans = product.find_all('span') 
            for span in spans:
                span_text = span.text.strip()
                if span_text == 'In Stock':
                    in_stock = True
                elif span_text == 'Out Of Stock':
                    in_stock = False

            # Append product data to list
            data.append({
                'title': title,
                'price': price,
                'link': link,
                'in_stock': in_stock,
                'store': 'sigma'
            })

        logging.info('✅finshed scrapping sigma')
        return data

    except Exception as e:
        logging.error(f'❌ Sigma scraper failed: {e}')
        raise
