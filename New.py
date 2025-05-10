import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

# --- Config ---
SEARCH_KEYWORDS = ["laptop", "smartphone", "headphones"]
ECOMMERCE_URL = "https://www.ubuy.co.in/category/laptops-21457"
SCREENSHOT_DIR = "du_Screenshot"

# --- Setup ---
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
driver.maximize_window()
wait = WebDriverWait(driver, 10)

seen_ids = {}

def extract_item_id_from_page():
    """
    Extract the real item ID from product detail page using <span id="item_id">
    """
    try:
        item_element = wait.until(EC.presence_of_element_located((By.ID, "item_id")))
        return item_element.text.strip()
    except Exception as e:
        print(f"❌ Error extracting Item ID from page: {e}")
        return None

def save_screenshot_of_card(card, item_id, index):
    folder = os.path.join(SCREENSHOT_DIR, item_id)
    os.makedirs(folder, exist_ok=True)
    screenshot_path = os.path.join(folder, f"duplicate_{index}.png")

    driver.execute_script("arguments[0].scrollIntoView(true);", card)
    time.sleep(1)

    location = card.location
    size = card.size

    driver.save_screenshot("temp_full.png")
    image = Image.open("temp_full.png")

    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    if right <= left or bottom <= top:
        print(f"⚠️ Invalid crop dimensions for Item ID {item_id}. Skipping screenshot.")
        return

    image = image.crop((left, top, right, bottom))
    image.save(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")

def search_and_check(keyword):
    print(f"\n🔍 Searching for: {keyword}")
    driver.get(ECOMMERCE_URL)

    try:
        # Wait and scroll to search box
        search_box = wait.until(EC.visibility_of_element_located((By.NAME, "q")))
        driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
        time.sleep(1)

        search_box.click()
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        time.sleep(4)

        product_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.listing-product")))

        for index, card in enumerate(product_cards):
            try:
                link_elem = card.find_element(By.CSS_SELECTOR, "a")
                product_url = link_elem.get_attribute("href")

                # Open detail page in new tab
                driver.execute_script("window.open(arguments[0]);", product_url)
                driver.switch_to.window(driver.window_handles[-1])

                item_id = extract_item_id_from_page()
                if not item_id:
                    print(f"⚠️ No valid Item ID found for: {product_url}")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                print(f"🔎 Item ID found: {item_id}")

                if item_id in seen_ids:
                    seen_ids[item_id] += 1
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    save_screenshot_of_card(card, item_id, seen_ids[item_id])
                else:
                    seen_ids[item_id] = 1
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"❌ Error on product card {index}: {e}")
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"❌ Error during search for '{keyword}': {e}")

# Run all keywords
for keyword in SEARCH_KEYWORDS:
    search_and_check(keyword)

driver.quit()
