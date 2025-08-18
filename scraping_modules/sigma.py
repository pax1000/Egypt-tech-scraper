import requests
from bs4 import BeautifulSoup
import logging
import re
import time
import random

def sigma_scraper(product_name):
    logging.info('🔍 scraping sigma...')
    data = []
    page_number = 1

    while True:
        try:
            url = f"https://www.sigma-computer.com/en/search?q={product_name}&page={page_number}"
            r = requests.get(url, timeout=40)
            soup = BeautifulSoup(r.text, "html.parser")

            # Find all product blocks
            products = soup.select(
                "div.flex.flex-col.gap-1.py-3.hover\\:border-\\[\\#3181b9\\].relative."
                "transition-all.select-none.border-\\[\\#D9EBF7\\]."
                "dark\\:border-sigma-blue-dark-light.border.h-full.bg-white."
                "dark\\:bg-gray-800.rounded-2xl.css-0"
            )
            if not products:  # stop when no more products
                break

            for product in products:
                try:
                    main_section = product.select_one("div.px-2")

                    # Title and link
                    link_tag = main_section.select_one("a")
                    title = link_tag.text.strip()
                    link = 'https://www.sigma-computer.com' + link_tag.get('href')

                    # Price
                    price_tag = product.select_one('p.font-bold')
                    price = price_tag.text.strip() if price_tag else None

                    # Stock status
                    in_stock = True
                    badges_container = main_section.select_one('div#badges-container')
                    if badges_container and "Out Of Stock" in badges_container.text:
                        in_stock = False

                    # Save product
                    data.append({
                        'title': title,
                        'price': price,
                        'link': link,
                        'in_stock': in_stock,
                        'store': 'sigma'
                    })
                except Exception as e:
                    logging.warning(f"⚠️ failed to parse product on page {page_number}: {e}")

            print(f'finished scraping page {page_number}')
            page_number += 1
            time.sleep(random.uniform(1, 3))  # polite delay

            # detect last page
            last_page_btn = soup.find("button", attrs={"aria-label": re.compile(r"last page, page \d+")})
            if last_page_btn:
                last_page = int(last_page_btn.text.strip())
                if page_number > last_page:
                    break

        except Exception as e:
            logging.error(f'❌ sigma scraper failed: {e}')
            break

    logging.info('✅ Finished scraping sigma')
    return data

