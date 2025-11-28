from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# Launch browser
driver = webdriver.Chrome()
driver.get("http://automationexercise.com")
driver.maximize_window()

# Step 1: Wait for the page to load by checking for an element or title
try:
    WebDriverWait(driver, 20).until(  # Increase the timeout if needed
        EC.presence_of_element_located((By.XPATH, "//div[@class='logo pull-left']"))
    )
    print("Desired page opened")
except Exception as e:
    print(f"Error: Homepage didn't load properly. Exception: {e}")
    driver.quit()
    exit()  # Exit if the homepage didn't load properly

# Step 2: Continue with the rest of your actions
# Click on signup/login link
signup = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//i[@class='fa fa-lock']"))
)
signup.click()

# Verify signup page opened
expected_url = "https://automationexercise.com/login"
WebDriverWait(driver, 10).until(
    EC.url_contains("login")
)

if expected_url in driver.current_url:
    print("Signup page opened successfully")
else:
    print("Error: Signup page didn't open")
    driver.quit()
    exit()

# Continue with the rest of your logic...

# Step 2: Click on signup/login link
signup = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//i[@class='fa fa-lock']"))
)
signup.click()

# Verify if signup page opened successfully
expected_url = "https://automationexercise.com/login"
WebDriverWait(driver, 10).until(
    EC.url_contains("login")
)

if expected_url in driver.current_url:
    print("Signup page opened successfully")
else:
    print("Error: Signup page didn't open")
    driver.quit()
    exit()

# Step 3: Enter signup credentials
name_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//input[@data-qa='signup-name']"))
)
name_field.send_keys("TukaRam Bhide")

email_field = driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
email_field.send_keys("lithemgfvvvoch4x929@ehtramay.com")

signup_btn = driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")
signup_btn.click()

# Step 4: Wait for the next page to load
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[@class='title text-center']"))
)

# Verify that we are on the account creation page
try:
    account_info_header = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'b'))
    )
    print("Account Information page is visible")
except Exception as e:
    print(f"Error: Account Information page not displayed. Exception: {e}")
    driver.quit()
    exit()

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
        driver.quit()
        exit()

except Exception as e:
    print(f"Error: Could not verify account creation. Exception: {e}")
    driver.quit()
    exit()

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
    driver.quit()
    exit()

# Step 10: Delete Account
driver.find_element(By.XPATH, "//i[@class='fa fa-trash-o']").click()

# Step 11: Verify Account Deletion
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-deleted']"))
)

try:
    account_deleted_header = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-deleted' and text()='Account Deleted']"))
    )
    print("Account deleted successfully")
except Exception as e:
    print(f"Error: Account not deleted. Exception: {e}")

# Step 12: Close browser
time.sleep(3)
driver.quit()
