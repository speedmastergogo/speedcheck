from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time
import os

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://automationexercise.com/")

Contact = driver.find_element(By.XPATH,"//i[@class='fa fa-envelope']")
Contact.click()


excepted_url = "https://automationexercise.com/contact_us"
#print(driver.current_url)
if excepted_url == driver.current_url:
    print("contact us form is opened")
else:
    print("error: unable to open contact us form")

#Filling details 
def filling_details():
    driver.find_element(By.XPATH,'//input[@data-qa="name"]').send_keys('jethalal gada')
    driver.find_element(By.XPATH,'//input[@data-qa="email"]').send_keys('jethalal123@gmail.com')
    driver.find_element(By.XPATH,'//input[@data-qa="subject"]').send_keys('refrigerator and mobile phones')
    driver.find_element(By.XPATH,'//textarea[@data-qa="message"]').send_keys('googlegooglegooglegooglegooglegooglegooglegooglegooglegooglegooglegooglegooglegoogle')
    file_input = driver.find_element(By.XPATH,'//input[@name="upload_file"]')
    path = "/home/u-64/Pictures/yes.png"
    print(os.path.exists(path))
    file_input.send_keys(path)
    time.sleep(3)
    
filling_details()
submit = driver.find_element(By.XPATH,'//input[@data-qa="submit-button"]')
submit.click()
WebDriverWait(driver, 10).until(EC.alert_is_present())
alert = driver.switch_to.alert
alert.accept()
time.sleep(2)
Success = driver.find_element(By.XPATH,'//div[@class="status alert alert-success"]').text
if "Success! Your details have been submitted successfully." in Success:
    print("verifcation done")
else:
    print("error: try again")

Home = driver.find_element(By.XPATH,'//a[@class="btn btn-success"]')
Home.click()
logo = driver.find_element(By.XPATH, '//img[@alt="Website for automation practice"]')  
if logo.is_displayed():
    print("Logo is displayed")
else:
    print("Logo is NOT displayed")

time.sleep(3)
driver.quit()


# chat gpt code 
'''from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Locators (Best practice)
CONTACT_BTN = (By.XPATH, "//i[@class='fa fa-envelope']")
NAME_FIELD = (By.XPATH, '//input[@data-qa="name"]')
EMAIL_FIELD = (By.XPATH, '//input[@data-qa="email"]')
SUBJECT_FIELD = (By.XPATH, '//input[@data-qa="subject"]')
MESSAGE_BOX = (By.XPATH, '//textarea[@data-qa="message"]')
UPLOAD_FILE = (By.XPATH, '//input[@name="upload_file"]')
SUBMIT_BTN = (By.XPATH, '//input[@data-qa="submit-button"]')
SUCCESS_MSG = (By.XPATH, '//div[@class="status alert alert-success"]')
HOME_BTN = (By.XPATH, '//a[@class="btn btn-success"]')
LOGO_IMG = (By.XPATH, '//img[@alt="Website for automation practice"]')


def open_contact_form():
    driver.get("https://automationexercise.com/")
    wait.until(EC.element_to_be_clickable(CONTACT_BTN)).click()
    assert driver.current_url == "https://automationexercise.com/contact_us", \
        "Failed to open Contact Us page"
    print("Contact Us page opened successfully.")


def fill_contact_form():
    wait.until(EC.visibility_of_element_located(NAME_FIELD)).send_keys("jethalal gada")
    driver.find_element(*EMAIL_FIELD).send_keys("jethalal123@gmail.com")
    driver.find_element(*SUBJECT_FIELD).send_keys("refrigerator and mobile phones")
    driver.find_element(*MESSAGE_BOX).send_keys("google" * 20)

    # Upload file
    file_path = "/home/u-64/Pictures/yes.png"
    assert os.path.exists(file_path), "File not found!"
    driver.find_element(*UPLOAD_FILE).send_keys(file_path)
    print("Form filled and file uploaded successfully.")


def submit_form():
    driver.find_element(*SUBMIT_BTN).click()

    # Wait for alert
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    print("Alert handled successfully.")


def verify_success_message():
    msg = wait.until(EC.visibility_of_element_located(SUCCESS_MSG)).text
    assert "Success! Your details have been submitted successfully." in msg, \
        "Success message not found!"
    print("Form submission verified successfully.")


def verify_logo_visible():
    logo = wait.until(EC.visibility_of_element_located(LOGO_IMG))
    assert logo.is_displayed(), "Logo not visible!"
    print("Logo is displayed correctly.")


# Execute steps
open_contact_form()
fill_contact_form()
submit_form()
verify_success_message()

driver.find_element(*HOME_BTN).click()
verify_logo_visible()

driver.quit()'''
