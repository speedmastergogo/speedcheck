from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()
driver.get("https://www.wikipedia.org/")
#assert "wikipedia" in driver.title
elem =driver.find_element(By.NAME,"search")
elem.clear()
elem.send_keys("Burj Khalifa")
elem.send_keys(Keys.RETURN)
#assert "not in results found" not in driver.page_source
time.sleep(2)
try:
    paras = driver.find_elements(By.CSS_SELECTOR, ".mw-parser-output > p")

    for p in paras:
         text = p.text.strip()
         if text:  # skip empty paragraphs
              print(text)
except:
    print("No short description found.")

driver.quit()