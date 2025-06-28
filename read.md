# Product Price Scraper

A multi-threaded web scraping application that monitors product prices across multiple Egyptian e-commerce stores and tracks price changes in a MySQL database.

## Features

- **Multi-store scraping**: Scrapes products from 4 different stores:
  - ElNekhely
  - ElBadrGroupEG
  - CompuMarts
  - Sigma

- **Price tracking**: Automatically tracks price changes and maintains price history
- **Smart scheduling**: Runs weekly based on most searched products
- **Multi-threading**: Uses multiprocessing for efficient concurrent scraping
- **Retry mechanism**: Implements retry logic for failed scraping attempts
- **Data validation**: Cleans and validates scraped data before storage

## Project Structure

```
├── main.py                     # Main scheduler and entry point
├── data_collection.py          # Handles multi-threaded scraping coordination
├── data_formater.py           # Cleans and formats scraped data
├── db_product_updater.py      # Database operations (insert/update/query)
├── scraping_modules/          # Individual store scrapers
│   ├── elnekhely.py
│   ├── elbadrgroupeg.py
│   ├── compumarts.py
│   └── sigma.py
├── time.json                  # Tracks last scraping date
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Prerequisites

- Python 3.7+
- MySQL database
- Chrome/Chromium browser (for Selenium)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd product-price-scraper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DB_HOST=your_database_host
   DB_PORT=3306
   DB_USER=your_username
   DB_PASS=your_password
   DB_NAME=your_database_name
   ```

4. **Database setup**
   Create the required tables in your MySQL database:
   ```sql
   CREATE TABLE products_info (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(500) NOT NULL,
       price DECIMAL(10,2) NOT NULL,
       link VARCHAR(1000) NOT NULL UNIQUE,
       in_stock BOOLEAN DEFAULT TRUE,
       store VARCHAR(100) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE price_history (
       id INT AUTO_INCREMENT PRIMARY KEY,
       product_id INT,
       old_price DECIMAL(10,2),
       new_price DECIMAL(10,2),
       changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (product_id) REFERENCES products_info(id)
   );

   CREATE TABLE most_searched (
       id INT AUTO_INCREMENT PRIMARY KEY,
       product_name VARCHAR(255) NOT NULL,
       search_count INT DEFAULT 0
   );
   ```

## Usage

### Running the Scraper

**Automatic scheduling (recommended):**
```bash
python main.py
```
This runs the scheduler which:
- Checks if a week has passed since last scraping
- Fetches the top 10 most searched products
- Scrapes all stores for these products
- Updates the database with new prices and price changes

**Manual scraping:**
```python
from data_collection import merging_data
from db_product_updater import add_to_database

# Scrape a specific product
product_name = "laptop"
scraped_data = merging_data(product_name)
add_to_database(scraped_data)
```

### Setting up Cron Job (Linux/Mac)

For automated weekly execution:
```bash
# Edit crontab
crontab -e

# Add this line to run every day at 2 AM (the script will check if a week has passed)
0 2 * * * /usr/bin/python3 /path/to/your/project/main.py
```

## Configuration

### Retry Settings
Modify retry attempts in `data_collection.py`:
```python
number_of_retries = 3  # Change this value
```

### Multiprocessing Pool Size
Adjust concurrent processes in `data_collection.py`:
```python
with multiprocessing.Pool(processes=2) as pool:  # Change processes count
```

### Scheduling Interval
Modify the scheduling interval in `main.py`:
```python
if difference >= 7:  # Change to desired number of days
```

## Data Format

The scraper standardizes product data into this format:
```python
{
    'title': str,      # Product title
    'price': float,    # Numeric price
    'link': str,       # Product URL (cleaned)
    'in_stock': bool,  # Availability status
    'store': str       # Store name
}
```

## Error Handling

- **Network errors**: Automatic retry with exponential backoff
- **Database errors**: Handles duplicate entries and connection issues
- **Data validation**: Skips products with missing critical information
- **Logging**: Comprehensive logging for monitoring and debugging

## Logging

The application uses Python's logging module with INFO level. Logs include:
- Scraping progress and results
- Database operations
- Error messages with retry information
- Scheduling status

## Performance Considerations

- Uses multiprocessing for concurrent store scraping
- Implements connection pooling for database operations
- Includes sleep delays to respect website rate limits
- Cleans URLs to avoid duplicate entries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add scrapers for new stores in `scraping_modules/`
4. Update the scraper list in `data_collection.py`
5. Test thoroughly
6. Submit a pull request

## Adding New Stores

To add a new store scraper:

1. Create a new file in `scraping_modules/new_store.py`
2. Implement a scraper function that returns standardized data format
3. Add the import and function to `data_collection.py`:
   ```python
   from scraping_modules.new_store import new_store_scraper
   
   scraper_functions = [sigma_scraper, elnekhely_scraper, 
                       elbadrgroupeg_scraper, compumarts_scraper, 
                       new_store_scraper]  # Add here
   ```

## Troubleshooting

**Common issues:**

1. **Chrome driver issues**: Ensure Chrome/Chromium is installed
2. **Database connection**: Verify credentials in `.env`
3. **Permission errors**: Check file permissions for `time.json`
4. **Memory issues**: Reduce multiprocessing pool size

**Debug mode:**
Set logging level to DEBUG for verbose output:
```python
logging.basicConfig(level=logging.DEBUG)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and personal use only. Always respect websites' robots.txt and terms of service. Be mindful of scraping frequency to avoid overwhelming target servers.