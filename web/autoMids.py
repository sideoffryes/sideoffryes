from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
from datetime import datetime

def get_schedule(driver):
    # Get user input about alpha
    ALPHA = ""
    cmd = input("(1) Use 251854\n(2) Enter custom alpha\ncmd> ")
    if cmd == "1":
        ALPHA = "251854"
    elif cmd == "2":
        ALPHA = input("Enter custom alpha> ")
    else:
        print("ERROR! Invalid command.\nExiting...")
        exit(1)

    print(f"Querying schedule for {ALPHA} on MIDS...")

    # select Midshipmen button
    mid_button = driver.find_element(by=By.CSS_SELECTOR, value="#mainmenu > tbody > tr:nth-child(1) > td:nth-child(3) > a:nth-child(3)")
    mid_button.click()

    # select query midn schedule link
    schedule_link = driver.find_element(by=By.CSS_SELECTOR, value="body > table > tbody > tr > td:nth-child(3) > li:nth-child(42) > a")
    schedule_link.click()

    # select alpha box
    alpha_box = driver.find_element(by=By.CSS_SELECTOR, value="#P_ALPHA")
    alpha_box.send_keys(ALPHA)

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

def get_photos(driver):
    # get and validate company
    company = input("Enter company to query> ")
    if int(company) < 1 or int(company) > 36:
        print("ERROR! Invalid company selection.\nExiting...")
        exit(2)

    year = input("Enter class year to query> ")
    if int(year) < 2023 or int(year) > 2028:
        print("Error! Invalid class year selection.\nExiting...")
        exit(3)

    # get mids page
    driver.get("https://mids.usna.edu")

    # select Midshipmen button
    mid_button = driver.find_element(by=By.CSS_SELECTOR, value="#mainmenu > tbody > tr:nth-child(1) > td:nth-child(3) > a:nth-child(3)")
    mid_button.click()

    # Select query photos link
    photos_button = driver.find_element(by=By.CSS_SELECTOR, value="body > table > tbody > tr > td:nth-child(3) > li:nth-child(32) > a")
    photos_button.click()

    # Select company box
    co_list = driver.find_element(by=By.CSS_SELECTOR, value="#P_MICO_CO_NBR")
    co_list.send_keys(company)
    co_list.send_keys(Keys.ENTER)

    # Select class year box
    year_list = driver.find_element(by=By.CSS_SELECTOR, value="#P_CLYE_CLASS_APPLIED_FOR")
    year_list.send_keys(year)
    year_list.send_keys(Keys.ENTER)

    # submit form
    find_button = driver.find_element(by=By.CSS_SELECTOR, value="body > form:nth-child(11) > p:nth-child(2) > input[type=submit]:nth-child(4)")
    find_button.click()

    # make sure pics directory exists first
    now = datetime.now()
    timestamp = now.strftime("%d%b%Y-%H_%M_%S")
    path = f"./pics/{timestamp}-{company}-{year}"
    os.makedirs(path)

    table_rows = driver.find_elements(by=By.CLASS_NAME, value="cgrldatarow")

    for row in table_rows:
        cells = row.find_elements(by=By.TAG_NAME, value="td")
        for c in cells:
            # Extract name
            name = c.find_element(by=By.TAG_NAME, value="font").text
            name = name.replace("/", " ")
            name = name.split()
            
            # change formatting if they don't have a middle name or have 2 middle names 
            # 1 middle name
            if len(name) == 5:
                fname = f"{name[0][0]}{name[1][0]}{name[2]}"
            # 2 middle names
            elif len(name) == 6:
                fname = f"{name[0][0]}{name[1][0]}{name[2][0]}{name[3]}"
            # No middle name
            elif len(name) == 4:
                fname = f"{name[0][0]}{name[1]}"
            # idk whatever else
            else:
                fname = f"{name[0]}"

            # Extract image URL
            img = c.find_element(by=By.TAG_NAME, value="img")
            url = img.get_attribute("src")
            urllib.request.urlretrieve(url, f"{path}/{fname}.jpg")

def load_mids(driver):
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

if __name__ == "__main__":
    # Set up Chrome driver
    # ignore certificate stuff
    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    # Set implicit wait time
    driver.implicitly_wait(15)

    # load in mids
    load_mids(driver)

    # get user commands
    print("(1) Query Schedule\n(2) Batch Photo Download")
    cmd = input("cmd> ")

    if cmd == "1":
        get_schedule(driver)
    elif cmd == "2":
        get_photos(driver)
    else:
        print("ERROR! Invalid command.\nExiting...")
        exit(2)

    driver.close()