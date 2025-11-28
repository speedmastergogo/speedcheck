from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import  Keys
import time
driver = webdriver.Chrome()
def Open_browser():
    driver.get("https://practicetestautomation.com/practice-test-login/")
    driver.maximize_window()
def valid_login():
     Login=driver.find_element(By.ID,"username")
     Login.send_keys("student")
     Password=driver.find_element(By.ID,"password")
     Password.send_keys("Password123")
     submit=driver.find_element(By.ID,"submit")
     submit.click()
     expected_url="practicetestautomation.com/logged-in-successfully/"
     if expected_url in driver.current_url:
          print("URL verification passed")
     else:
          print("false")
     page_text = driver.find_element(By.TAG_NAME,"strong").text
     if "Congratulations" in page_text:
         print("verification complete")
     else:
         print("false")    
     logout=driver.find_element(By.LINK_TEXT,"Log out").text
     if "Log out" in logout:
          print("verify")
     else:
       print("false")
def wrong_username():
    Login=driver.find_element(By.ID,"username")
    Login.send_keys("ssss")
    Password=driver.find_element(By.ID,"password")
    Password.send_keys("Password123")
    submit=driver.find_element(By.ID,"submit")
    submit.click()
    error_message = driver.find_element(By.ID,"error").text
    if  "Your username is invalid!" not in error_message:
        print("error message is displayed")
    elif "Your username is invalid!"  in error_message:
        print("error meaasge displayed and text is Your username is invalid!")
    
def wrong_password():
    Login=driver.find_element(By.ID,"username")
    Login.send_keys("student")
    Password=driver.find_element(By.ID,"password")
    Password.send_keys("Password1523")
    submit=driver.find_element(By.ID,"submit")
    submit.click()
    error_message = driver.find_element(By.ID,"error").text
    if  "Your password is invalid!" not in error_message:
        print("error message is displayed")
    elif "Your password is invalid!"  in error_message:
        print("error meaasge displayed and text is Your password is invalid!")
    
Open_browser()
valid_login()

Open_browser()
wrong_username()

Open_browser()
wrong_password()

time.sleep(5)
driver.quit()