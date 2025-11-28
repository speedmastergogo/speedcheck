from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://automationexercise.com/")
wait = WebDriverWait(driver,10)
if driver.current_url == "https://automationexercise.com/":
    print("homepage opened successfully")
else:
    print("unable to homepage")

def products():
    driver.find_element(By.CSS_SELECTOR,"a[href='/products']").click()
    time.sleep(5)
products()
def add_product(n):
    product = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, f".product-image-wrapper:nth-of-type({n})")
    ))

    img = product.find_element(By.CSS_SELECTOR, "img")

    # Scroll a bit above to avoid ad iframe
    driver.execute_script("window.scrollBy(0, -200);")
    driver.execute_script("arguments[0].scrollIntoView(true);", img)
    driver.execute_script("window.scrollBy(0, -150);")  # important shift!

    actions = ActionChains(driver)

    # Hover the image
    actions.move_to_element(img).perform()

    # Move slightly inside overlay to avoid iframe intercept
    actions.move_by_offset(0, -40).perform()

    # Now wait for the Add to cart button
    add_cart = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f".product-image-wrapper:nth-of-type({n}) .add-to-cart")
    ))

    # Click via JavaScript to avoid iframe issues completely
    driver.execute_script("arguments[0].click();", add_cart)

    # Close modal
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".close-modal")
    )).click()


add_product(1)   # first product
add_product(2)

#def first_product1():'''
'''# Locate product image
    first2 = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[3]//div[1]//div[1]//div[1]//img[1]")))

    # Scroll into view to avoid iframe overlap
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first2)


    # Hover over the product
    actions = ActionChains(driver)
    actions.move_to_element(first2).perform()

    # Wait until overlay Add to cart becomes clickable
    add_cart = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".overlay-content a[data-product-id='2']")))

    add_cart.click()

    # Close modal
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn.btn-success.close-modal.btn-block"))).click()

#first_product1()'''
''

time.sleep(5)
driver.quit()