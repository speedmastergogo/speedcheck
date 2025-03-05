import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_driver_path = '/usr/local/bin/chromedriver'

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering (optional, for better compatibility)
chrome_options.add_argument("--window-size=1366,699")  # Set window size (optional but recommended)

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


#keywords = ['fresh fruits', 'fresh apple', 'tripod']

# Array of product keywords
keywords = [
    "headphones", "laptop", "phone", "shoes", "watch", "tablet", "camera", "monitor", 
    "keyboard", "mouse", "charger", "printer", "blender", "backpack", "toaster", "microwave", 
    "speaker", "sofa", "pillow", "vacuum", "bicycle", "jacket", "treadmill", "bookshelf", 
    "router", "fan", "grill", "chair", "mirror", "bed", "desk", "lamp", "oven", "fridge", 
    "mixer", "stroller", "bottle", "clock", "mattress", "umbrella", "iron", "freezer", 
    "razor", "headset", "notebook", "projector", "detergent", "airpods", "tripod", "sneakers", 
    "tent", "tripod", "kettle", "wallet", "jewelry", "perfume", "perfume", "makeup", 
    "sunglasses", "telescope", "t-shirt", "hoodie", "dress", "shorts", "pants", 
    "blanket", "curtains", "rug", "fan", "bracelet", "ring", "necklace", "earrings", 
    "plushie", "speaker", "scooter", "luggage", "purse", "carpet", "toys", 
    "guitar", "ukulele", "piano", "batteries", "socks", "boots", "gloves", 
    "camera lens", "flashlight", "lunchbox", "cushion", "tablet stand", 
    "yoga mat", "electric toothbrush", "robot vacuum", "fitness tracker", 
    "smart bulb", "water filter", "frying pan", "slow cooker", "portable fan"
]

selected_keywords = random.sample(keywords, 10)

# Lists to store response times
list_page_times = []
detail_page_times = []
not_found = 0  # Counter for not found
is_out_of_stock = 0 # Counter for oos products


for product in selected_keywords:
    try:
        driver.get("https://www.u-buy.co.nz")
        driver.set_window_size(1366, 699)

        search_box = driver.find_element(By.CSS_SELECTOR, ".ds-input")
        search_box.clear()  # Clear any previous input
        search_box.send_keys(product)
        start_time = time.time()
        search_box.send_keys(Keys.ENTER)

        # Wait for the search results to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-3:nth-child(4) .product-title"))
        )
        end_time = time.time()
        response_time_list = end_time - start_time
        list_page_times.append(response_time_list)

        print(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

        # Click on the first product
        driver.find_element(By.CSS_SELECTOR, ".col-lg-3:nth-child(4) .img-detail img").click()

        # Wait for the product detail page to load and check the availability status (either 'In stock' or 'Out of stock')
        try:
            WebDriverWait(driver, 20).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock.ms-1")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"))
                )
            )
            
            end_time = time.time()
            response_time_detail = end_time - start_time - response_time_list 
            detail_page_times.append(response_time_detail)

            # Check if product is Not found or out of stock
            if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                print(f"Keyword: {product} - Product is out of stock")
                is_out_of_stock +=1

            elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                print(f"Keyword: {product} - Product Not found")
                not_found +=1

            print(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1000:.2f} ms")

        except:
            print(f"Keyword: {product} - timeout.")


    except Exception as e:
        print(f"An error occurred for keyword '{product}': {e}")

    finally:
        # Navigate back to the main URL to start with the next keyword
        driver.get("https://www.u-buy.co.nz")
        driver.set_window_size(1366, 699)

driver.quit()


# Calculate and print min and max response times
if list_page_times:
    list_min = min(list_page_times)
    list_max = max(list_page_times)

if detail_page_times:
    detail_min = min(detail_page_times)
    detail_max = max(detail_page_times)
    print(f"The list page is taking time around {list_min:.2f} to {list_max:.2f} sec to load, and detail page is taking time around {detail_min:.2f} to {detail_max:.2f} sec to load. (NZ)")

# Print the not founds and oos
print(f"Not founds: {not_found}")
print(f"out_of_stocks: {is_out_of_stock}")
