import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Config ---
SEARCH_KEYWORDS = ["laptop", "smartphone", "headphones"]
ECOMMERCE_URL = "https://www.ubuy.co.in/"  # Replace with real URL
SCREENSHOT_DIR = "du_Screenshot"

# --- Setup ---
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

driver = webdriver.Chrome()  # Make sure ChromeDriver is in PATH
driver.maximize_window()

wait = WebDriverWait(driver, 10)

def save_duplicate_screenshot(card, keyword, index, product_name):
    # Create a folder for the product name if it doesn't exist
    product_folder = os.path.join(SCREENSHOT_DIR, product_name)
    if not os.path.exists(product_folder):
        os.makedirs(product_folder)

    # Define screenshot file path
    screenshot_path = os.path.join(product_folder, f"{product_name}_{keyword}_duplicate_{index}.png")
    
    location = card.location
    size = card.size

    # Ensure location and size are valid before proceeding
    if not location or not size:
        print(f"❌ Invalid location or size for card {index}. Skipping screenshot.")
        return

    # Take a full screenshot
    driver.save_screenshot("temp_full.png")

    # Check if the screenshot was successfully saved
    if os.path.exists("temp_full.png"):
        print("Temporary screenshot file saved!")
    else:
        print("Error: Temporary screenshot not saved.")
        return

    image = Image.open("temp_full.png")

    # Get the crop coordinates (left, top, right, bottom)
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    # Validate the crop dimensions
    if left < 0 or top < 0 or right <= left or bottom <= top:
        print(f"❌ Invalid crop dimensions for card {index}. Skipping crop.")
        return

    # Crop the image to the specific card size
    image = image.crop((left, top, right, bottom))

    # Save the cropped image
    image.save(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")

    # Check if the image is valid and viewable
    try:
        image.verify()  # Verify image integrity
        print(f"✅ Screenshot is valid and saved: {screenshot_path}")
    except Exception as e:
        print(f"❌ Error verifying image: {e}")

def search_and_check(keyword):
    print(f"\n🔍 Searching for: {keyword}")
    driver.get(ECOMMERCE_URL)

    try:
        # Wait until search box is present and interactable
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

        # Scroll to the search box just in case it is off-screen
        driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
        time.sleep(0.5)

        # Inject keyword and submit using JS
        driver.execute_script("arguments[0].value = arguments[1];", search_box, keyword)
        search_box.submit()

        time.sleep(3)  # Wait for the page to load results

        titles_seen = {}  # Store already seen products
        product_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.listing-product")))  # Wait for product cards to load

        for index, card in enumerate(product_cards):
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, ".product-title")  # Update selector if needed
                title_text = title_elem.text.strip()

                # Check if the product title is a duplicate
                if title_text in titles_seen:
                    print(f"⚠️ Duplicate found: {title_text}")

                    # Scroll to the duplicate product card
                    driver.execute_script("arguments[0].scrollIntoView();", card)
                    time.sleep(1)

                    # Save the screenshot of the duplicate product
                    save_duplicate_screenshot(card, keyword, index, title_text)

                else:
                    titles_seen[title_text] = 1

            except Exception as e:
                print(f"❌ Error with product card {index}: {e}")

    except Exception as e:
        print(f"❌ Error during search for '{keyword}': {e}")

# Run the search and check for each keyword
for word in SEARCH_KEYWORDS:
    search_and_check(word)

driver.quit()
