from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

# ignore certificate stuff
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

# let it redirect and load to get the popup
driver.implicitly_wait(15)

# get mids page
driver.get("https://mids.usna.edu")


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

# Get all rows in the table
table_rows = driver.find_elements(by=By.CLASS_NAME, value="cgrldatarow")

# get data from each row
max_len = 0
cell_text_list = []
for row in table_rows:
    cells = row.find_elements(by=By.TAG_NAME, value="td")

    curr_cell = []
    # print out contents of each cell
    for c in cells:
        if len(c.text) > max_len:
            max_len = len(c.text)
        curr_cell.append(c.text)

    cell_text_list.append(curr_cell)

for cell in cell_text_list:
    for i in range(len(cell)):
        if i == 0:
            print(f"{cell[i]:^{max_len}}", end="")
        else:
            print(f"{cell[i]:^{max_len - 5}}", end="")
    print()

driver.close()