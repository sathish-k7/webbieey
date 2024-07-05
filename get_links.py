import requests
import time
import signal
import sys
from test import extractor

class LinkFetcher:
    def __init__(self, server_url, interval=1):
        self.server_url = server_url
        self.interval = interval
        self.unique_links = set()
        self.running = True

    def fetch_links(self):
        try:
            response = requests.get(f'{self.server_url}/get_links')
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            links = data.get('links', [])

            for link in links:
                if link not in self.unique_links:
                    self.unique_links.add(link)
                    print(f"Unique link found and processed: {link}")
                    extractor(link, 'output.json')
                    print('\n')

        except requests.exceptions.RequestException as e:
            print(f"Error fetching links: {e}")

    def periodic_fetch(self):
        while self.running:
            self.fetch_links()
            time.sleep(self.interval)

    def stop(self):
        self.running = False

def signal_handler(sig, frame):
    print('Received signal to stop, shutting down...')
    fetcher.stop()
    sys.exit(0)

if __name__ == '__main__':
    fetcher = LinkFetcher(server_url='http://127.0.0.1:5000', interval=5)

    # Handle termination signals for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    fetcher.periodic_fetch()
