def formater(data):
    import re
    new_data = []
    for product in data:
        title = product.get('title', '').strip()
        price_str = str(product.get('price', '')).strip()
        product_link = product.get('link', '').strip()
        in_stock = product.get('in_stock', False)
        store = product.get('store', '').strip()
        product_link = re.sub(pattern='\?search.*',repl='',string=product_link)
        # Skip if critical data is missing
        if '' in (title, price_str, product_link):
            continue
        
        price_str = price_str.replace(",", "")
        price_str = re.sub(r'\.0+', '', price_str)

        # Extract numeric price safely
        match = re.search(r'\d+\.?\d*', price_str)
        if not match:
            continue  # skip if no valid price found

        try:
            price = float(match.group())
        except ValueError:
            continue

        new_data.append({
            'title': title,
            'price': price,
            'link': product_link,
            'in_stock': in_stock,
            'store': store
        })
    return new_data






