from selectorlib import Extractor
import requests 
from time import sleep

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):  
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

    # Download the page using requests
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)

    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None

    # Extract data using Selectorlib
    return e.extract(r.text)

def write_product_details(outfile, product_details):
    outfile.write(f"Product Title: {product_details['name']}\n")
    outfile.write(f"Price: {product_details['price']}\n")
    outfile.write(f"Short Description:\n{product_details['short_description']}\n")
    outfile.write(f"Product Description:\n{product_details['product_description']}\n")
    outfile.write(f"Images: {', '.join(product_details['images'])}\n")
    outfile.write(f"Rating: {product_details['rating']}\n")
    outfile.write(f"Number of Reviews: {product_details['number_of_reviews']}\n")
    outfile.write(f"Link to All Reviews: {product_details['link_to_all_reviews']}\n")
    outfile.write("\n")

# Read URLs from the file and extract product details
with open("urls.txt", 'r') as urllist, open('output.txt', 'w', encoding='utf-8') as outfile:
    for url in urllist.read().splitlines():
        data = scrape(url) 
        if data:
            write_product_details(outfile, data)
