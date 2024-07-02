from selectorlib import Extractor
import requests
import json
import time
from urllib.parse import urljoin

# Create Extractors by reading from the YAML files
product_extractor = Extractor.from_yaml_file('selectors.yml')


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

    url = urljoin(base_url, relative_url)
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None
    
    # Extract reviews
    data = product_extractor.extract(r.text)
    top_positive_review = data.get('top_positive_review', 'No positive review found')
    top_critical_review = data.get('top_critical_review', 'No critical review found')
    
    return {'top_positive_review': top_positive_review, 'top_critical_review': top_critical_review}

def write_product_details(outfile, product_details):
    for key, value in product_details.items():
        if key == 'top_positive_review' or key == 'top_critical_review':
            outfile.write(f"{key}: {value}\n")
        else:
            outfile.write(f"{key}: {value}\n")
    outfile.write("\n")  # Separate different products with a newline

with open("urls.txt", 'r') as urllist, open('output.txt', 'w') as outfile:
    for url in urllist.read().splitlines():
        product_details = scrape_product_details(url)
        if product_details and 'link_to_all_reviews' in product_details:
            reviews = scrape_reviews(url, product_details['link_to_all_reviews'])
            product_details.update(reviews)
        else:
            product_details['top_positive_review'] = 'No positive review found'
            product_details['top_critical_review'] = 'No critical review found'

        with open('output.txt', 'a', encoding='UTF-8') as outfile:
            write_product_details(outfile, product_details)
