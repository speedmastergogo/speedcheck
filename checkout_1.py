from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
driver = webdriver.Chrome(options=chrome_options)
import time

#launch the browser
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://automationexercise.com/")
wait = WebDriverWait(driver,10)
#homepage verification
logo = driver.find_element(By.XPATH,"//img[@alt='Website for automation practice']")
#print("logo:",logo)
assert logo.is_displayed(),"homepage is not opened"
print("homepage opened succesfully")

#add product into cart
def addtocart():
    product = wait.until(EC.visibility_of_element_located((By.XPATH,"(//img[@alt='ecommerce website products'])[4]")))
    view = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a[href='/product_details/4']")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", view)
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(product).perform()
    time.sleep(3)
    clickcart = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > section:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(3)")))
    clickcart.click()
    wait.until(EC.visibility_of_element_located((By.XPATH,"//u[normalize-space()='View Cart']"))).click()
    #print("clickcart",clickcart)
    assert driver.current_url == "https://automationexercise.com/view_cart", "cart page is not opened "
    print("cart page opened successfully")
addtocart()
def register():
    signup = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='fa fa-lock']")))
    signup.click()

# Verify if signup page opened successfully
    expected_url = "https://automationexercise.com/login"
    WebDriverWait(driver, 10).until(
    EC.url_contains("login"))

    if expected_url in driver.current_url:
     print("Signup page opened successfully")
    else:
     print("Error: Signup page didn't open")
    

# Step 3: Enter signup credentials
    name_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//input[@data-qa='signup-name']")))
    name_field.send_keys("TukaRam Bhide")

    email_field = driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
    email_field.send_keys("liuucgecceg988@ehtramay.com")

    signup_btn = driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")
    signup_btn.click()

# Step 4: Wait for the next page to load
    WebDriverWait(driver, 10).until(
      EC.visibility_of_element_located((By.XPATH, "//h2[@class='title text-center']")) )

# Verify that we are on the account creation page
    try:
          account_info_header = WebDriverWait(driver, 15).until(
             EC.visibility_of_element_located((By.TAG_NAME, 'b')))
          print("Account Information page is visible")
    except Exception as e:
         print(f"Error: Account Information page not displayed. Exception: {e}")
    
# Step 5: Fill out account details
    gender_radio = driver.find_element(By.ID, 'uniform-id_gender1')
    gender_radio.click()

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys('testing@123')

    # Select Date, Month, Year
    Select(driver.find_element(By.ID, "days")).select_by_visible_text("15")
    Select(driver.find_element(By.ID, "months")).select_by_visible_text("June")
    Select(driver.find_element(By.ID, "years")).select_by_visible_text("2011")

    # Check newsletter and opt-in
    driver.find_element(By.ID, "newsletter").click()
    driver.find_element(By.ID, "optin").click()

    # Fill out personal details
    driver.find_element(By.ID, 'first_name').send_keys("TukaRam")
    driver.find_element(By.ID, 'last_name').send_keys("Bhide")
    driver.find_element(By.ID, 'company').send_keys("Dholakpur")
    driver.find_element(By.ID, 'address1').send_keys("Near Singham Returns, Dholakpur")
    driver.find_element(By.ID, 'address2').send_keys("Tappu Sena")
    Select(driver.find_element(By.ID, 'country')).select_by_visible_text("United States")
    driver.find_element(By.ID, 'state').send_keys("Washington DC")
    driver.find_element(By.ID, 'city').send_keys("DC")
    driver.find_element(By.ID, 'zipcode').send_keys("41018")
    driver.find_element(By.ID, 'mobile_number').send_keys('8974587488')

    # Step 6: Click Create Account button
    create_account_btn = driver.find_element(By.XPATH, "//button[@data-qa='create-account']")
    create_account_btn.click()

    # Step 7: Verify Account Creation
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-created']"))
    )

    try:
        account_created_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-created']/b"))
        ).text
        print(account_created_message)
        if "ACCOUNT CREATED!" in account_created_message:
            print("Account created successfully")
        else:
            print("Error: Account not created")
           
    except Exception as e:
        print(f"Error: Could not verify account creation. Exception: {e}")
      
    # Step 8: Click Continue after account creation
    continue_btn = driver.find_element(By.LINK_TEXT, 'Continue')
    continue_btn.click()

    # Step 9: Verify that user is logged in
    try:
        logged_in_header = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//a[text()=' Logged in as ']"))
        )
        print("Logged in successfully")
    except Exception as e:
        print(f"Error: Login failed. Exception: {e}")
        
register()
#click on cart
def cart():
    wait.until(EC.visibility_of_element_located((By.XPATH,"//a[normalize-space()='Cart']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='Proceed To Checkout']"))).click()
cart()
#print delivery adress

'''delivery_addres = driver.find_element(By.CSS_SELECTOR,"#address_delivery").text
billing_address = driver.find_element(By.CSS_SELECTOR,"#address_invoice").text
print(repr(delivery_addres))
print(repr(billing_address))

assert delivery_addres == billing_address ,"not verified"
print("address verified successfully")'''
# -----------------------------
#  ADDRESS VERIFICATION
# -----------------------------

def normalize_address(text):
    lines = text.split("\n")
    address_lines = lines[1:]   # skip "YOUR DELIVERY ADDRESS" / "YOUR BILLING ADDRESS"
    cleaned = [line.strip() for line in address_lines if line.strip()]
    return "\n".join(cleaned)

delivery_raw = driver.find_element(By.CSS_SELECTOR, "#address_delivery").text
billing_raw = driver.find_element(By.CSS_SELECTOR, "#address_invoice").text

print("RAW DELIVERY:", repr(delivery_raw))
print("RAW BILLING:", repr(billing_raw))

delivery_address = normalize_address(delivery_raw)
billing_address = normalize_address(billing_raw)

print("CLEAN DELIVERY:", delivery_address)
print("CLEAN BILLING:", billing_address)

assert delivery_address == billing_address, "❌ Address mismatch!"
print("✔ Address verified successfully!")


# -----------------------------
#  REVIEW ORDER (1 PRODUCT)
# -----------------------------
def verify_single_product():
    # Product Name
    name = driver.find_element(By.XPATH, "//a[normalize-space()='Stylish Dress']").text.strip()

    # Price → Rs. 500 → 500
    price_text = driver.find_element(By.CSS_SELECTOR, "td.cart_price p").text.strip()
    price = int(price_text.replace("Rs.", "").strip())

    # Quantity (input box)
    quantity = int(driver.find_element(By.CSS_SELECTOR, ".disabled").get_attribute("value"))

    # Total shown on UI
    total_text = driver.find_element(By.CSS_SELECTOR, "td.cart_total p.cart_total_price").text.strip()
    ui_total = int(total_text.replace("Rs.", "").strip())

    # Expected total
    expected_total = price * quantity

    print("\n--- PRODUCT INFO ---")
    print("Product Name:   ", name)
    print("Price:          ", price)
    print("Quantity:       ", quantity)
    print("UI Total:       ", ui_total)
    print("Expected Total: ", expected_total)

    assert ui_total == expected_total, "❌ Total price mismatch!"
    print("✔ Single product verified successfully!")


# RUN THE PRODUCT VERIFICATION
verify_single_product()

    
driver.quit() 
