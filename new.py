from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)

# Path to your ChromeDriver
chrome_driver_path = '/usr/local/bin/chromedriver'

# Create a Service object for ChromeDriver
service = Service(executable_path=chrome_driver_path)

try:
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Record the start time
    start_time = time.time()

    # Open Google
    driver.get("https://www.google.com")

    # Locate the search box and enter the search query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("laptops")
    search_box.submit()

    # Wait for the results to load (adjust the wait time as needed)
    driver.implicitly_wait(10)

    # Record the end time
    end_time = time.time()

    # Calculate the response time
    response_time = end_time - start_time
    print(f"Response time: {response_time:.2f} seconds")

finally:
    # Close the WebDriver
    driver.quit()





"""for product in selected_keywords:
    try:
        driver.get("https://www.a.ubuy.com.kw/en/")
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

        # Wait for the product detail page to load
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "add-to-cart-btn"))
            )
            end_time = time.time()
            response_time_detail = end_time - start_time - response_time_list
            detail_page_times.append(response_time_detail)

            print(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1000:.2f} ms")
        
        except:
            print(f"Keyword: {product} - 'Add to cart' button not found within the given time.")
            no_add_to_cart_count += 1

    except Exception as e:
        print(f"An error occurred for keyword '{product}': {e}")

    finally:
        # Navigate back to the main URL to start with the next keyword
        driver.get("https://www.a.ubuy.com.kw/en/")
        driver.set_window_size(1366, 699)

driver.quit()
"""
