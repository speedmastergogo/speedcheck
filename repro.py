from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
# launch the browser
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://automationexercise.com/")
wait = WebDriverWait(driver,10)
logo = wait.until(EC.visibility_of_element_located((By.XPATH,"//img[@alt='Website for automation practice']")))

assert logo.is_displayed(),"Homepage is not opened successfully"
print("Home page opened successfully")

#add products into the cart 
def addtocart():
    product = wait.until(EC.visibility_of_element_located((By.XPATH,"(//img[@alt='ecommerce website products'])[1]")))
    view = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a[href='/product_details/1']")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", view)
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(product).perform()
    time.sleep(3)
    clickcart = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > section:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(3)")))
    clickcart.click()
    wait.until(EC.visibility_of_element_located((By.XPATH,"//u[normalize-space()='View Cart']"))).click()
    #print("clickcart",clickcart)
    assert driver.current_url == "https://automationexercise.com/view_cart", "cart page is not opened "
    print("cart page opened successfully")
addtocart()
time.sleep(3)
def delete_cart():
    delete = wait.until(EC.visibility_of_element_located((By.XPATH,"//tr[@id='product-1']//i[@class='fa fa-times']")))
    delete.click()
    emtcart = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"p[class='text-center'] b")))
    print(emtcart)
    assert emtcart.is_displayed(),"cart is not empty"
    print("cart is empty")
delete_cart()
time.sleep(3)
driver.quit()
