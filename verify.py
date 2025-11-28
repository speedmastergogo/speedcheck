from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://automationexercise.com/")
wait = WebDriverWait(driver,10)
if driver.current_url == "https://automationexercise.com/":
    print("homepage opened successfully")
else:
    print("not verfied")
def open_detail():
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a[href='/product_details/2']"))).click()
    assert driver.current_url == "https://automationexercise.com/product_details/2" , "detail page is not opened"
    print("detail page opened")
open_detail()
def in_qty(target):
    qty = driver.find_element(By.XPATH,'//input[@id="quantity"]')
    actions = ActionChains(driver)
    actions.move_to_element(qty).perform()
    current = int(qty.get_attribute("value"))

    while current < target:
        qty.send_keys(Keys.ARROW_UP)     # Increase qty
        time.sleep(0.2)
        current = int(qty.get_attribute("value"))

in_qty(4)
def ad_cart():
    driver.find_element(By.XPATH,"//button[normalize-space()='Add to cart']").click()
    wait.until(EC.visibility_of_element_located((By.XPATH,"//u[normalize-space()='View Cart']"))).click()
ad_cart()
cart_qty = wait.until( EC.visibility_of_element_located((By.XPATH, "//td[contains(@class, 'cart_quantity')]/button")))
elem = driver.find_element(By.XPATH, "//td[@class='cart_quantity']")
print(elem.get_attribute("innerHTML"))

print("Cart qty found:", repr(cart_qty))
assert cart_qty == "4", "Quantity mismatch"
print("added desired quantity")
time.sleep(4)
driver.quit()