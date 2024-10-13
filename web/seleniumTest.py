from selenium import webdriver
from selenium.webdriver.common.by import By

# set chrome as our browser
driver = webdriver.Chrome()

# get page
driver.get("https://www.selenium.dev/documentation/webdriver/getting_started/first_script/")

# get browser title
title = driver.title

# let page load before grabbing elements
driver.implicitly_wait(2)

page_title = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div.td-main > div > main > div > h1")
print(page_title.text)
# text_box.send_keys("Test")

driver.quit()