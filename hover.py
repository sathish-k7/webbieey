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

# Open the e-commerce website
website_url = 'https://www.amazon.in/s?k=headphones&crid=2LYIZ008ISSMO&sprefix=head%2Caps%2C232&ref=nb_sb_ss_ts-doa-p_2_4'
driver.get(website_url)

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

driver.execute_script(hover_script)

print("Hover over products to capture their URLs. Close the browser window when done...")

# Python list to store the URLs
urls_list = []

# Wait for the user to manually hover over products
while True:
    try:
        time.sleep(1)  # Check every second
        hovered_urls = driver.execute_script("return window.getHoveredURLs();")
        # Extend the list to avoid nested lists
        urls_list.extend([url for url in hovered_urls if url not in urls_list])
    except:
        # Browser window closed
        break

# Close the browser
driver.quit()

# Print all captured URLs
print("Captured Product URLs:")
for url in urls_list:
    print(url)
print(f"Total URLs captured: {len(urls_list)}")

# Write captured URLs to urls.txt
with open('urls.txt', 'w') as file:
    for url in urls_list:
        file.write(url + '\n')

print("URLs saved to urls.txt")
