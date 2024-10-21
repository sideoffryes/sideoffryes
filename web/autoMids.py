import os
import time
import urllib.request
from datetime import datetime

from colorama import Back, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

#TODO: Webserver?

init(autoreset=True)

def get_schedule(driver):
    # Get user input about alpha
    ALPHA = ""
    cmd = input("(1) Use 251854\n(2) Enter custom alpha\n(3) Back to Menu\ncmd> ")

    match cmd:
        case "1":
            ALPHA = "251854"
        case "2":
            ALPHA = input("Enter custom alpha> ")
        case "3":
            return
        case _:
            print(Back.RED + "ERROR! Invalid command.")
            cmd = input("(1) Use 251854\n(2) Enter custom alpha\n(3) Back to Menu\ncmd> ")

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
    while int(company) < 1 or int(company) > 36:
        print("ERROR! Invalid company selection.")
        company = input("Enter company to query> ")

    year = input("Enter class year to query> ")
    while int(year) < 2023 or int(year) > 2028:
        print("Error! Invalid class year selection.")
        year = input("Enter class year to query> ")

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

def free_period_finder(driver):
    # Company validation
    co_num = input("Company Number> ")
    while int(co_num) < 1 or int(co_num) > 36:
        print(Back.RED + "ERROR! Invalid company selected. Select from [1-36]")
        co_num = input("Company Number> ")
    
    # Day validation
    while True:
        # convert day to index
        day = input("Day of the week [M T W R F]> ")
        match day:
            case "M":
                day = 1
                break
            case "T":
                day = 2
                break
            case "W":
                day = 3
                break
            case "R":
                day = 4
                break
            case "F":
                day = 5
                break
            case _:
                print(Back.RED + "ERROR! Invalid day selected. Select from [M T W R F]")
    
    # Period validation
    period = int(input("Period [1-7]> "))
    while period < 1 or period > 7:
        print(Back.RED + "ERROR! Invalid class period selected. Select from [1-7]")
        period = int(input("Period [1-7]> "))

    # get mids page
    driver.get("https://mids.usna.edu")

    # select midshipmen link
    mid_button = driver.find_element(by=By.CSS_SELECTOR, value="#mainmenu > tbody > tr:nth-child(1) > td:nth-child(3) > a:nth-child(3)")
    mid_button.click()

    # Select schedules link
    schedules = driver.find_element(by=By.CSS_SELECTOR, value="body > table > tbody > tr > td:nth-child(3) > li:nth-child(42) > a")
    schedules.click()

    # Select company box
    co_box = driver.find_element(by=By.CSS_SELECTOR, value="#P_MICO_CO_NBR")
    co_box.send_keys(co_num)

    # Branch for if looking up a group or just 1 mid
    print(f"Select Search Type:\n(1) Individual\n(2) Group")
    search_type = input("cmd> ")

    if search_type == "1":
        individual_search(driver, period, day)
    elif search_type == "2":
        group_search(driver, period, day)
    else:
        print(Back.RED + "ERROR! Invalid search type selected.")

def individual_search(driver, period, day):
    print(f"Enter the individual's alpha")
    alpha = input("Alpha> ")

    alpha_box = driver.find_element(by=By.XPATH, value='//*[@id="P_ALPHA"]')
    alpha_box.send_keys(alpha)

    # Submit form
    find_button = driver.find_element(by=By.CSS_SELECTOR, value="body > form:nth-child(8) > p:nth-child(2) > input[type=submit]:nth-child(4)")
    find_button.click()

    # Get name
    name = driver.find_element(by=By.XPATH, value="/html/body/h3/table/tbody/tr/td[1]/font/b/font").text
    name = name.replace("/", " ")
    name = name.split()

    if len(name) == 4:
        name = f"{name[0]} {name[1]}"
    elif len(name) == 5:
        name = f"{name[0]} {name[2]}"
    else:
        name = f"{name[0]}"

    # get rows from table
    rows = driver.find_elements(by=By.CSS_SELECTOR, value="body > table > tbody > tr")
    period_row = rows[period + 1]
    cells = period_row.find_elements(by=By.TAG_NAME, value="td")
    day_cell = cells[day]
    course = day_cell.text

    if course == " ":
        print(Back.GREEN + f"{name} HAS A FREE PERIOD")
    else:
        print(Back.RED + f"{name} HAS {course}")

def group_search(driver, period, day):
    # get class years to search
    print(f"Enter class years to search, separated with spaces [2025 - 2028]")
    years = input("years> ").split()
    years = [y[2:] for y in years]
    print("YEARS TO SEARCH: ", years)

    # Submit form
    find_button = driver.find_element(by=By.CSS_SELECTOR, value="body > form:nth-child(8) > p:nth-child(2) > input[type=submit]:nth-child(4)")
    find_button.click()

    # save list of links on the page
    links = []
    # get rows from table on first page
    rows = driver.find_elements(by=By.CLASS_NAME, value="cgrldatarow")
    for r in rows:
        alpha = r.find_element(by=By.CSS_SELECTOR, value="td > font > a").text
        y = alpha[:2]
        if y in years:
            schedule_link = r.find_element(by=By.CSS_SELECTOR, value="td > font > a")
            links.append(schedule_link.get_attribute("href"))

    # Go to the next page and get the rest of the links
    next = driver.find_element(by=By.XPATH, value="/html/body/form/input[11]")
    next.click()
    
    # get rows from table on first page
    rows = driver.find_elements(by=By.CLASS_NAME, value="cgrldatarow")
    for r in rows:
        alpha = r.find_element(by=By.CSS_SELECTOR, value="td > font > a").text
        y = alpha[:2]
        if y in years:
            schedule_link = r.find_element(by=By.CSS_SELECTOR, value="td > font > a")
            links.append(schedule_link.get_attribute("href"))

    # visit each of the links
    for l in links:
        # load page with schedule
        driver.get(l)

        # Get name
        name = driver.find_element(by=By.XPATH, value="/html/body/h3/table/tbody/tr/td[1]/font/b/font").text
        name = name.replace("/", " ")
        name = name.split()

        if len(name) == 4:
            name = f"{name[0]} {name[1]}"
        elif len(name) == 5:
            name = f"{name[0]} {name[2]}"
        else:
            name = f"{name[0]}"

        # get rows from table
        rows = driver.find_elements(by=By.CSS_SELECTOR, value="body > table > tbody > tr")
        period_row = rows[period + 1]
        cells = period_row.find_elements(by=By.TAG_NAME, value="td")
        day_cell = cells[day]
        course = day_cell.text

        if course == " ":
            print(Back.GREEN + f"{name} HAS A FREE PERIOD")
        else:
            print(Back.RED + f"{name} HAS {course}")

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
    # options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    # Set implicit wait time
    driver.implicitly_wait(15)

    # load in mids
    load_mids(driver)

    # get user commands
    while True:
        print("(1) Query Schedule\n(2) Batch Photo Download\n(3) Free Period Finder\n(4) Exit")
        cmd = input("cmd> ")

        match cmd:
            case "1":
                get_schedule(driver)
            case "2":
                get_photos(driver)
            case "3":
                free_period_finder(driver)
            case "4":
                driver.close()
                exit(0)
            case _:
                print(Back.RED + "ERROR! Invalid command.")