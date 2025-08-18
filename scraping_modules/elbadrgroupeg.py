import cloudscraper
from bs4 import BeautifulSoup
import logging

def elbadrgroupeg_scraper(product_name):
    logging.info('🔍 scraping elbadrgroupeg...')  # Log the start of the scraping process

    data = []  # List to store product info
    page_number = 1  # Start from the first page

    # Create a CloudScraper session (handles Cloudflare)
    scraper = cloudscraper.create_scraper()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    while True:
        try:
            # Construct the search URL with the product name and current page
            url = f"https://elbadrgroupeg.store/index.php?route=product/search&search={product_name}&page={page_number}"
            
            # Use cloudscraper to get the page
            r = scraper.get(url, headers=headers, timeout=40)
            soup = BeautifulSoup(r.text, 'html.parser')

            # Find all product blocks; stop the loop if none found
            products_container = soup.find('div', class_='main-products')
            if not products_container or not products_container.find_all('div', class_='product-layout'):
                logging.warning(f"No products found on page {page_number}. First 500 chars of response:\n{r.text[:500]}")
                break

            main_products = products_container.find_all('div', class_='product-layout')

            for product in main_products:
                # Extract the product title and link
                name_block = product.find('div', class_='name').find('a')
                title = name_block.text.strip()
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
                price_div = product.find('div', class_='price')
                if price_div:
                    price_spans = price_div.find_all('span')
                    for span in price_spans:
                        classes = span.get('class', [])
                        if any(cls in ['price-normal', 'price-new'] for cls in classes):
                            price = span.text.strip()

                # Add the product data to the list
                data.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'in_stock': in_stock,
                    'store': 'elbadrgroupeg'
                })

            logging.info(f'finished scraping this page {page_number}')
            page_number += 1  # Move to next page

        except Exception as e:
            logging.error(f'there was an error as {e}')  # Log the error
            break

    logging.info('✅finshed scrapping elbadrgroupeg')  # Log completion
    return data
