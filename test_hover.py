'''from selenium import webdriver
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
import pytest
driver = webdriver.Chrome()

driver.get("https://www.a.ubuy.com.kw/en/")
driver.maximize_window()
@pytest.mark.others
def test_hover_dropdown():
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
test_hover_dropdown()
driver.quit
 '''
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    # Setup Chrome options
    options = Options()
    # options.add_argument("--headless")  # Uncomment to run in headless mode
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver  # This will provide the driver to the test function
    driver.quit()  # Cleanup after the test function has finished

def test_hover_dropdown(driver):
    driver.get("https://www.a.ubuy.com.kw/en/")
    
    # Locate the category element
    category = driver.find_element(By.ID, "explore-category")
    
    # Perform the hover action
    actions = ActionChains(driver)
    actions.move_to_element(category).perform()
    
    # Wait until the category dropdown is visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "explore-category"))
    )
    
    # Click on the "Health & Supplements" category link
    click1 = driver.find_element(By.LINK_TEXT, "Health & Supplements")
    click1.click()
    
    # Verify the URL after clicking
    expected_url = "https://www.a.ubuy.com.kw/en/category/health-supplements-10019"
    assert expected_url in driver.current_url, f"Expected URL to be {expected_url}, but got {driver.current_url}"

