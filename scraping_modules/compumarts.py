import requests
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.INFO,)



def compumarts_scraper(product_name):
    logging.info('🔍 scraping compumarts...')
    
    data = []  # List to store scraped product data
    page_number = 1  # Start from page 1

    while True:
        try:
            # Set headers to mimic a real browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }

            # Send GET request to the search results page
            r = requests.get(
                f'https://www.compumarts.com/search?options[prefix]=last&page={page_number}&q={product_name}',
                headers=headers,
                timeout=40
            )
            soup = BeautifulSoup(r.text, 'html.parser')

            # Get the main products container; break if not found
            results_container = soup.find('div', class_='main-products-grid__results')
            if not results_container or not results_container.find('ul'):
                break

            main_products = results_container.find('ul')
            products = main_products.find_all('li', class_='js-pagination-result')

            for product in products:
                # Extract product title and link
                name_block = product.find('a', class_='card-link')
                title = name_block.text
                link = 'https://www.compumarts.com' + name_block.get('href')

                # Try to extract the price; skip item if missing
                try:
                    price = product.find('span', class_='js-value').text
                except:
                    continue

                # Default to in stock unless "Sold out" is found
                in_stock = True
                label_container = product.find('span', class_='product-label--sold-out')
                if label_container:
                    if label_container.text.strip() == 'Sold out':
                        in_stock = False

                # Append product data to the result list
                data.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'in_stock': in_stock,
                    'store': 'compumarts'
                })

            print(f'finished scraping this page {page_number}')
            page_number += 1  # Move to next page

        except Exception as e:
            logging.error(f'❌ compumarts scraper failed: {e}')
            break

    logging.info('✅finshed scrapping compumarts')
    return data

