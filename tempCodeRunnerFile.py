from selectorlib import Extractor
import requests
import json
import time
from urllib.parse import urljoin

# Create Extractors by reading from the YAML files
product_extractor = Extractor.from_yaml_file('selectors.yml')
search_extractor = Extractor.from_yaml_file('search_results.yml')

def scrape_product_details(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None
    
    # Extract product details
    data = product_extractor.extract(r.text)
    return data

def scrape_reviews(base_url, relative_url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    reviews = {'positive': None, 'critical': None}
    url = urljoin(base_url, relative_url)
    while url and not (reviews['positive'] and reviews['critical']):
        print("Downloading %s" % url)
        r = requests.get(url, headers=headers)
        if r.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in r.text:
                print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
            return None
        
        # Pass the HTML of the page and create 
        data = product_extractor.extract(r.text)
        if data and 'reviews' in data:
            for review in data['reviews']:
                # Assuming structure of review might be different, adjust as per your actual data
                rating = review.get('review_rating', '')  # Get review rating if available
                if rating.startswith('5.0') and not reviews['positive']:
                    reviews['positive'] = review.get('review_text', '')
                elif rating.startswith('1.0') and not reviews['critical']:
                    reviews['critical'] = review.get('review_text', '')
            url = urljoin(base_url, data.get('next_page')) if data.get('next_page') else None
            time.sleep(2)  # Be respectful and don't hit the server too frequently
        else:
            url = None
    
    return reviews

def write_product_details(outfile, product_details):
    for key, value in product_details.items():
        if key == 'reviews':
            outfile.write(f"{key}:\n")
            outfile.write(f"  - Positive: {value['positive']}\n")
            outfile.write(f"  - Critical: {value['critical']}\n")
        elif key == 'product_description':
            outfile.write(f"{key}:\n")
            outfile.write(f"  - {value}\n")
        else:
            outfile.write(f"{key}: {value}\n")
    outfile.write("\n")  # Separate different products with a newline

def scrape_search_results(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None
    
    # Extract search results
    data = search_extractor.extract(r.text)
    return data

# Read URLs from the search results file and extract product data
search_results = []
with open("search_results_urls.txt", 'r') as urllist:
    for url in urllist.read().splitlines():
        data = scrape_search_results(url)
        if data:
            for product in data['products']:
                search_results.append(product)

# Read URLs from the product details file and extract detailed product data
with open("urls.txt", 'r') as urllist, open('output.txt', 'w') as outfile:
    for url in urllist.read().splitlines():
        product_details = scrape_product_details(url)
        if product_details and 'link_to_all_reviews' in product_details:
            reviews = scrape_reviews(url, product_details['link_to_all_reviews'])
            product_details['reviews'] = reviews
        else:
            product_details['reviews'] = {'positive': None, 'critical': None}

        # Match product details with search results to update price and rating
        for search_product in search_results:
            if search_product['title'] == product_details['name']:
                if not product_details.get('price'):
                    product_details['price'] = search_product.get('price')
                if not product_details.get('rating'):
                    product_details['rating'] = search_product.get('rating')
                break
        
        write_product_details(outfile, product_details)
