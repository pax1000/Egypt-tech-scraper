A Python-based scraper to extract product data (title, price, availability, and link) from three major Egyptian tech e-commerce websites. For now, it supports:

- [`elbadrgroupeg.store`](https://elbadrgroupeg.store/)
- [`elnekhelytechnology.com`](https://www.elnekhelytechnology.com/)
- [`sigma-computer.com`](https://www.sigma-computer.com/)
- [`compumarts.com`](https://www.compumarts.com/)

## 🚀 Features

- ✅ Scrapes real product data
- ✅ Filters out-of-stock items
- ✅ Supports infinite scroll and load-more buttons
- ✅ Outputs clean, structured JSON
- ✅ Runs in headless mode using Selenium

## 📁 Project Structure

root/
├── scrapers/
│ ├── elbadrgroupeg.py
│ ├── elnekhely.py
│ ├── compumarts.py
│ └── sigma.py
│
├── data.json
├── filtered.json
│ 
│
├── utils/ # Optional: helpers for scrolling/logging
│ └── helpers.py
│
├── requirements.txt
└── README.md

makefile
Copy
Edit

## 🧰 Libraries Used

```txt
selenium==4.19.0
seleniumbase==4.26.0


📝 Notes
This project is a work in progress.
more sites are to be added
A web interface and merged comparison output are planned .
