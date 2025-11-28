import time
import random
import streamlit as st 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Use your chromedriver path (as in your original)
chrome_driver_path = '/usr/local/bin/chromedriver'

# Prepare chrome options but DO NOT start driver globally.
# (Driver will be created only when Run Test is pressed.)
def make_chrome_options(headless=False):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1366,699")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # uncomment if you want headless; by default keep visible for debugging
    chrome_options.add_argument("--headless=new")
    

service = Service(executable_path=chrome_driver_path)

st.title('Ubuy Speed Check')

selected_location = None

# Display buttons for location selection using session state
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button('QA'):
        st.session_state.selected_location = 'QA'
with col2:
    if st.button('KW'):
        st.session_state.selected_location = 'KW'
with col3:
    if st.button('UAE'):
        st.session_state.selected_location = 'UAE'

selected_location = st.session_state.selected_location

if selected_location:
    st.write(f"Calculating at: {selected_location}")
else:
    st.write("Please select a domain.")

# keep your keyword list (trimmed in this paste for brevity — keep your full list)
keywords = [
    "iphone 15 pro max", "samsung galaxy s24 ultra", "apple macbook air m2",
    "sony noise cancelling headphones", "wireless bluetooth neckband earphones",
    "portable mini bluetooth speaker", "4k ultra hd projector",
    "smart watch for women", "laptop stand with fan", "usb c charging cable",
    "nike air force shoes", "adidas ultra boost sneakers", "men leather wrist watch",
    "women crossbody shoulder bag", "stylish polarized sunglasses men",
    "designer analog wrist watch", "lightweight running sports shoes",
    "women floral printed dress", "men slim fit jeans", "leather casual formal shoes",
    "water bottle stainless steel", "automatic electric rice cooker",
    "non stick frying pan", "air fryer digital display", "electric kettle with filter",
    "coffee maker with grinder", "hand blender with whisk", "cordless vacuum cleaner handheld",
    "led touch table lamp", "wall mounted clothes hanger",
    "playstation 5 wireless controller", "xbox series x console", "nintendo switch oled model",
    "gaming chair with footrest", "rgb backlit gaming keyboard", "wireless gaming mouse pad",
    "gaming headset with mic", "curved gaming monitor 27", "racing steering wheel setup",
    "gaming desk with light", "baby stroller travel system", "baby feeding bottle set",
    "newborn baby gift set", "educational building block toy", "soft plush teddy bear",
    "remote control racing car", "children waterproof digital watch",
    "kids drawing color set", "baby diaper changing mat", "baby sleeping carry bag",
    "hair dryer with diffuser", "ceramic hair straightening brush",
    "rechargeable electric beard trimmer", "waterproof facial cleansing brush",
    "moisturizing face cream women", "matte liquid lipstick set",
    "anti dandruff shampoo men", "compact travel makeup mirror",
    "organic aloe vera gel", "stainless steel nail clipper",
    "yoga mat with strap", "stainless steel water flask", "hiking backpack waterproof travel",
    "portable outdoor camping stove", "foldable lightweight camping chair",
    "high speed skipping rope", "cycling helmet safety gear", "swimming goggles anti fog",
    "adjustable dumbbell weight set", "portable electric air pump",
    "automatic pet food dispenser", "cat litter cleaning scoop", "dog training shock collar",
    "retractable dog walking leash", "pet grooming brush comb", "indoor air purifying plant",
    "ultrasonic pest repellent device", "lint roller pet hair",
    "robotic vacuum cleaner mop", "odor eliminating air freshener",
    "wireless ergonomic computer mouse", "mechanical backlit typing keyboard",
    "laptop cooling pad stand", "adjustable mobile phone holder",
    "noise cancelling office headset", "portable document file organizer",
    "multi port usb hub", "external solid state drive", "laser wireless color printer",
    "office table desk lamp", "digital infrared forehead thermometer",
    "electric hot water bag", "reusable gel ice pack", "compression knee support sleeve",
    "adjustable posture correction belt", "automatic blood pressure monitor",
    "stainless steel kitchen scissors", "travel size toiletry bottles",
    "rechargeable led emergency light", "foldable multipurpose storage box"
]

selected_keywords = random.sample(keywords, min(12, len(keywords)))

list_page_times = []
detail_page_times = []
not_found = 0
is_out_of_stock = 0

# Reuse your run_tests functions but use options and start timers correctly
def run_tests_nz(driver, selected_keywords):
    global list_page_times, detail_page_times, not_found, is_out_of_stock
    domain = "(QA)"

    for product in selected_keywords:
        try:
            driver.get("https://www.ubuy.qa/en/")
            driver.set_window_size(1366, 699)
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ds-input"))
            )
            search_box.clear()  
            search_box.send_keys(product)

            # LIST PAGE timer
            start_time = time.time()
            search_box.send_keys(Keys.ENTER)

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1) .product-title"))
            )
            end_time = time.time()
            response_time_list = (end_time - start_time)
            list_page_times.append(response_time_list)
            st.write(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

            # click first product
            driver.find_element(By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1)").click()

            # DETAIL PAGE timer: start fresh after click
            detail_start = time.time()
            try:
                WebDriverWait(driver, 20).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                    )
                )
                detail_end = time.time()
                response_time_detail = (detail_end - detail_start)
                detail_page_times.append(response_time_detail)

                if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1
                elif driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1
                elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                    st.write(f"Keyword: {product} - Product Not found")
                    not_found +=1

                st.write(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1000:.2f} ms")
            except Exception:
                st.write(f"Keyword: {product} - timeout.")
        except Exception as e:
            st.write(f"An error occurred for keyword '{product}': {e}")
        finally:
           # reset to homepage for next run
           try:
               driver.get("https://www.ubuy.qa/en/")
               driver.set_window_size(1366, 699)
           except:
               pass

def run_tests_kw(driver, selected_keywords):
    global list_page_times, detail_page_times, not_found, is_out_of_stock
    domain = "(KW)"
    for product in selected_keywords:
        try:
            driver.get("https://www.a.ubuy.com.kw/en")
            driver.set_window_size(1366, 699)

            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ds-input"))
            )
            search_box.clear()  
            search_box.send_keys(product)

            # list timer
            start_time = time.time()
            search_box.send_keys(Keys.ENTER)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1) .product-title"))
            )
            end_time = time.time()
            response_time_list = (end_time - start_time)
            list_page_times.append(response_time_list)
            st.write(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

            driver.find_element(By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1)").click()

            # detail timer
            detail_start = time.time()
            try:
                WebDriverWait(driver, 20).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                    )
                )
                detail_end = time.time()
                response_time_detail = (detail_end - detail_start)
                detail_page_times.append(response_time_detail)

                if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1
                elif driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1
                elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                    st.write(f"Keyword: {product} - Product Not found")
                    not_found +=1

                st.write(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1000:.2f} ms")

            except:
                st.write(f"Keyword: {product} - timeout.")

        except Exception as e:
            st.write(f"An error occurred for keyword '{product}': {e}")

        finally:
            try:
                driver.get("https://www.a.ubuy.com.kw/en")
                driver.set_window_size(1366, 699)
            except:
                pass

def run_tests_uae(driver, selected_keywords):
    global list_page_times, detail_page_times, not_found, is_out_of_stock
    domain = "(UAE)"

    for product in selected_keywords:
        try:
            driver.get("https://www.ubuy.ae/en/")
            driver.set_window_size(1366, 699)

            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ds-input"))
            )
            search_box.clear()  
            search_box.send_keys(product)

            # list timer
            start_time = time.time()
            search_box.send_keys(Keys.ENTER)

            WebDriverWait(driver, 20).until(
               EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1) .product-title"))
            )
            end_time = time.time()
            response_time_list = (end_time - start_time)
            list_page_times.append(response_time_list)
            st.write(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

            driver.find_element(By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1)").click()

            # detail timer
            detail_start = time.time()
            try:
                WebDriverWait(driver, 20).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                    )
                )
                detail_end = time.time()
                response_time_detail = (detail_end - detail_start)
                detail_page_times.append(response_time_detail)

                if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1
                elif driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1
                elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                    st.write(f"Keyword: {product} - Product Not found")
                    not_found +=1

                st.write(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1000:.2f} ms")

            except:
                st.write(f"Keyword: {product} - timeout.")


        except Exception as e:
            st.write(f"An error occurred for keyword '{product}': {e}")

        finally:
            try:
                driver.get("https://www.ubuy.ae/en/")
                driver.set_window_size(1366, 699)
            except:
                pass

# Main logic to run tests
def main():
    # create driver only when user triggers the run
    chrome_options = make_chrome_options(headless=False)  # keep False to match your environment
    driver = webdriver.Chrome(service=service, options=chrome_options)

    if selected_location == 'QA':
        run_tests_nz(driver, selected_keywords)
    elif selected_location == 'KW':
        run_tests_kw(driver, selected_keywords)
    elif selected_location == 'UAE':
        run_tests_uae(driver, selected_keywords)

    driver.quit()

    avg_min_list = 3.00 
    avg_max_list = 6.00  

    avg_min_detail = 4.00 
    avg_max_detail = 8.00  

    less_than_avg_min_list = sum(1 for t in list_page_times if t < avg_min_list)
    greater_than_avg_max_list = sum(1 for t in list_page_times if t > avg_max_list)

    less_than_avg_min_detail = sum(1 for t in detail_page_times if t < avg_min_detail)
    greater_than_avg_max_detail = sum(1 for t in detail_page_times if t > avg_max_detail)


    if list_page_times:
        if less_than_avg_min_list <= 5:
            list_min = avg_min_list
        else:
            list_min = min(list_page_times)

        if greater_than_avg_max_list <= 3:
            list_max = avg_max_list
        else:
            list_max = max(list_page_times)

    if detail_page_times:
        if less_than_avg_min_detail <= 5:
            detail_min = avg_min_detail
        else:
            detail_min = min(detail_page_times)

        if greater_than_avg_max_detail <= 3:
            detail_max = avg_max_detail
        else:
            detail_max = max(detail_page_times)

        summary = (f"The list page is taking time around {list_min:.2f} to {list_max:.2f} sec to load, and "
                f"the detail page is taking time around {detail_min:.2f} to {detail_max:.2f} sec to load.({selected_location})\n")
        
        st.write(summary)
        st.write(f"Not founds: {not_found}\n" f"Out of stocks: {is_out_of_stock}")

if __name__ == "__main__":
    # run main only when clicking the Run button in the Streamlit UI
    if st.button("Run Tests"):
        main()
