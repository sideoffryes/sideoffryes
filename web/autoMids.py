from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

# ignore certificate stuff
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

# get mids page
driver.get("https://mids.usna.edu")

# let it redirect and load to get the popup
driver.implicitly_wait(3)

# get rid of popup
wait = WebDriverWait(driver, timeout=2)
alert = wait.until(lambda d : d.switch_to.alert)
alert.accept()

# submit username and password
# get boxes and submit button
user_box = driver.find_element(by=By.CSS_SELECTOR, value="#username")
pass_box = driver.find_element(by=By.CSS_SELECTOR, value="#password")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="#loginData > div.button-row > span > input")

# send info
user_box.send_keys("m251854")
pass_box.send_keys("HCFFall011708!?$")
submit_button.click()

# select Midshipmen button
mid_button = driver.find_element(by=By.CSS_SELECTOR, value="#mainmenu > tbody > tr:nth-child(1) > td:nth-child(3) > a:nth-child(3)")
mid_button.click()

# select query midn schedule link
schedule_link = driver.find_element(by=By.CSS_SELECTOR, value="body > table > tbody > tr > td:nth-child(3) > li:nth-child(42) > a")
schedule_link.click()

# select alpha box
alpha_box = driver.find_element(by=By.CSS_SELECTOR, value="#P_ALPHA")
alpha_box.send_keys("251854")

# select find button
find_button = driver.find_element(by=By.CSS_SELECTOR, value="body > form:nth-child(8) > p:nth-child(2) > input[type=submit]:nth-child(4)")
find_button.click()

# select schedule table
schedule = driver.find_element(by=By.CSS_SELECTOR, value="body > table")


time.sleep(5)

driver.close()