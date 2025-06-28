from scraping_modules.elnekhely import elnekhely_scraper
from scraping_modules.elbadrgroupeg import elbadrgroupeg_scraper
from scraping_modules.compumarts import compumarts_scraper
from scraping_modules.sigma import sigma_scraper
from data_formater import formater
import multiprocessing
import time
import logging


def scraper_with_retry(args):
    scraper_function, data = args
    number_of_retries = 3
    current = 0
    while current < number_of_retries:
        try:
            time.sleep(2)
            result = scraper_function(data)
            logging.info(f"{scraper_function.__name__} scraped {len(result)} items")
            return result
        except Exception as e:
            logging.error(f'There was an error: {e} in {scraper_function.__name__} number of retires left {number_of_retries - current}')
            current += 1
    return []


def merging_data(data):
    scraper_functions = [sigma_scraper, elnekhely_scraper, elbadrgroupeg_scraper, compumarts_scraper]
    tasks = [(func, data) for func in scraper_functions]
    with multiprocessing.Pool(processes=2) as pool:
        result = pool.map(scraper_with_retry, tasks)
    flat_result = [item for sublist in result for item in sublist]
    return(formater(flat_result))




