from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# =====================
# Disable Google Password Popup
# =====================
options = Options()
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})
options.add_argument("--disable-features=PasswordManagerOnboarding,PasswordImport")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

# =====================
# Open Login Page
# =====================
driver.get("https://www.saucedemo.com/")

# =====================
# Login
# =====================
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "user-name"))
).send_keys("standard_user")

driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

# Verify login success
WebDriverWait(driver, 10).until(
    EC.url_contains("inventory.html")
)
print("Login successful!")

# =====================
# Open Product Detail Page
# =====================
product = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[text()='Sauce Labs Fleece Jacket']"))
)
product.click()

WebDriverWait(driver, 10).until(
    EC.url_contains("inventory-item.html")
)
print("Product detail page opened!")

# =====================
# Add to Cart
# =====================
add_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'add-to-cart')]"))
)
add_btn.click()
print("Product added to cart!")

# =====================
# Verify Remove Button
# =====================
remove_btn = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//button[contains(@id,'remove')]"))
)

if remove_btn.text.lower() == "remove":
    print("✔ Product successfully added to cart!")
else:
    print("✘ Product not added to cart!")

time.sleep(2)
driver.quit()
