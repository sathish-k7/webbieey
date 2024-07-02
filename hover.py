from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from chromedriver_py import binary_path

# Specify the path to your ChromeDriver executable
driver_path = binary_path  # You can use the `binary_path` from chromedriver_py or specify your own path

# Set up the ChromeDriver service
service = Service(driver_path)

# Initialize the Chrome WebDriver with the specified service
driver = webdriver.Chrome(service=service)

# Inject JavaScript to detect hover events and capture URLs
hover_script = """
    var hoveredURLs = [];
    document.addEventListener('mouseover', function(event) {
        var element = event.target.closest('a');
        if (element && !hoveredURLs.includes(element.href)) {
            hoveredURLs.push(element.href);
            console.log('Hovered URL:', element.href);
        }
    });
    window.getHoveredURLs = function() {
        return hoveredURLs;
    };
"""

# Open the Amazon search results page
print("Please navigate to the Amazon search results page and hover over products to capture their URLs.")
print("Close the browser window when done...")

# Execute the hover script
driver.execute_script(hover_script)

# Python list to store the URLs
urls_list = []

# Continuously capture URLs while the browser is open
try:
    while True:
        time.sleep(1)  # Check every second
        hovered_urls = driver.execute_script("return window.getHoveredURLs();")
        new_urls = [url for url in hovered_urls if url not in urls_list]
        if new_urls:
            with open('urls.txt', 'a') as file:
                for url in new_urls:
                    file.write(url + '\n')
                    urls_list.append(url)
            print(f"Captured {len(new_urls)} new URLs")
except KeyboardInterrupt:
    print("User interrupted the process.")
finally:
    # Close the browser
    driver.quit()

# Print all captured URLs
print("Captured Product URLs:")
for url in urls_list:
    print(url)
print(f"Total URLs captured: {len(urls_list)}")

print("URLs saved to urls.txt")
