from selectorlib import Extractor
from summarizer import summarize_and_generate_points
import requests
import time
from urllib.parse import urljoin
import json
import os


product_extractor = Extractor.from_yaml_file('selectors.yml')

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


def check_status_code(response, url):
    if response.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in response.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, response.status_code))
        return False
    return True


def scrape_product_details(url):
    print(f"Scraping {url}")
    try:
        r = requests.get(url, headers=headers)
        if not check_status_code(r, url):
            return {}
        data = product_extractor.extract(r.text)
        return data if data else {}
    except Exception as e:
        print(f"Error scraping product details from {url}: {str(e)}")
        return {}


def scrape_reviews(base_url, relative_url):
    url = urljoin(base_url, relative_url)
    print(f"Scraping reviews from {url}")
    try:
        r = requests.get(url, headers=headers)
        if not check_status_code(r, url):
            return {}
        data = product_extractor.extract(r.text)
        return {
            'top_positive_review': data.get('top_positive_review', 'No positive review found'),
            'top_critical_review': data.get('top_critical_review', 'No critical review found')
        }
    except Exception as e:
        print(f"Error scraping reviews from {url}: {str(e)}")
        return {}


def write_product_details(outfile, product_details):
    if os.path.exists(outfile) and os.path.getsize(outfile) > 0:
        with open(outfile, 'r') as file:
            data = json.load(file)
    else:
        data = []
    if product_details not in data:
        data.append(product_details)
    with open(outfile, 'w') as file:
        json.dump(data, file, indent=4)


def extractor(input_file='urls.txt', output_file='output.json'):
    with open(input_file, 'r') as urllist:
        for url in urllist.read().splitlines():
            try:
                start_time = time.time()
                product_details = scrape_product_details(url)
                if product_details and 'link_to_all_reviews' in product_details:
                    reviews = scrape_reviews(url, product_details['link_to_all_reviews'])
                    product_details.update(reviews)
                else:
                    product_details['top_positive_review'] = 'No positive review found'
                    product_details['top_critical_review'] = 'No critical review found'

                write_product_details(output_file, product_details)
                key_points = summarize_and_generate_points(product_details['short_description'])
                print("\nGenerated Key Points:")
                for i, point in enumerate(key_points, 1):
                    print(f"{i}. {point.strip()}.")

                stop_time = time.time()
                print(f"Time taken to extract and summarize product details: {stop_time - start_time:.2f} seconds")

            except Exception as e:
                print(f"Error processing {url}: {str(e)}")

            # Optional: print a separator for better readability in the console
            print("-" * 50)


if __name__ == '__main__':
    extractor()
