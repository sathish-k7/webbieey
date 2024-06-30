from selectorlib import Extractor
import requests
import json
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Create Extractor from YAML files (selectors.yml and search_results.yml)

def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    print(f"Downloading {url}")
    r = requests.get(url, headers=headers)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print(f"Page {url} was blocked by Amazon. Please try using better proxies\n")
        else:
            print(f"Page {url} must have been blocked by Amazon as the status code was {r.status_code}")
        return None
    
    # Extract product details using BeautifulSoup
    product_details = extract_product_details(r.text)
    return product_details

def extract_product_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Example extraction based on your previous logic, adjust as needed
    product_name = soup.find('span', {'id': 'productTitle'}).get_text(strip=True)
    product_price = soup.find('span', {'id': 'priceblock_ourprice'}).get_text(strip=True)
    # Add more extraction logic as per your selectors.yml file or HTML structure
    
    # Example: extracting reviews
    reviews = scrape_reviews(soup)  # Implement scrape_reviews function
    
    # Example: extracting other product details
    product_details = {
        'name': product_name,
        'price': product_price,
        'reviews': reviews,
        # Add more details as needed
    }
    
    return product_details

def scrape_reviews(soup):
    reviews = {'positive': None, 'critical': None}
    
    # Implement your logic to scrape reviews
    # Example: scraping positive and critical reviews
    review_tags = soup.find_all('div', {'class': 'review'})  # Adjust selector as per your HTML structure
    
    for review in review_tags:
        review_rating = review.find('span', {'class': 'review-rating'}).get_text(strip=True)
        review_text = review.find('div', {'class': 'review-text'}).get_text(strip=True)
        
        if review_rating.startswith('5.0') and not reviews['positive']:
            reviews['positive'] = review_text
        elif review_rating.startswith('1.0') and not reviews['critical']:
            reviews['critical'] = review_text
        
        if reviews['positive'] and reviews['critical']:
            break
    
    return reviews

# Main script to read URLs from urls.txt and scrape details
with open('urls.txt', 'r') as urls_file, open('output.txt', 'w') as output_file:
    for url in urls_file:
        url = url.strip()
        if url:
            product_details = scrape_product_details(url)
            if product_details:
                # Write product details to output file
                output_file.write(json.dumps(product_details, indent=4) + '\n')
