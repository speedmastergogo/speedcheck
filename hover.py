from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#options = Options()
#options.add_argument("--headless")  # Run in headless mode
#options.add_argument("--no-sandbox")  # (recommended for Linux servers)
#options.add_argument("--disable-dev-shm-usage")  # (prevents memory issues)
#options.add_argument("--disable-gpu")  # Optional for Windows
import time
driver = webdriver.Chrome()

driver.get("https://www.a.ubuy.com.kw/en/")
driver.maximize_window()
def hover_dropdown():
 category = driver.find_element(By.ID,"explore-category")
 actions = ActionChains(driver)
 actions.move_to_element(category).perform()
 wait = WebDriverWait(driver, 10)
 element = wait.until(EC.visibility_of_element_located((By.ID, "explore-category")))
 click1 = driver.find_element(By.LINK_TEXT,"Health & Supplements")
 click1.click()
 Expected_url = "https://www.a.ubuy.com.kw/en/category/health-supplements-10019"
 if Expected_url in driver.current_url :
  print(" category opened successfully")
 else:
  print("error while opening category")

time.sleep(4)
hover_dropdown()
driver.quit
 