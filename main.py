import time
import os
import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from dotenv import load_dotenv

load_dotenv()

if not os.path.exists(".env"):
    print(".env file not found!")
    exit()

my_name = os.getenv("MY_NAME")
company_name = os.getenv("COMPANY_NAME")
company_description = os.getenv("COMPANY_DESCRIPTION")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
send_with_note = os.getenv("SEND_WITH_NOTE")

if (
    not my_name
    or not company_name
    or not company_description
    or not email
    or not password
):
    print("Please fill in all required fields in .env file!")
    exit()


# print welcome message
def print_green(text):
    print("\033[92m {}\033[00m".format(text))


def print_yellow(text):
    print("\033[93m {}\033[00m".format(text))


def print_red(text):
    print("\033[91m {}\033[00m".format(text))


# clear screen
os.system("cls" if os.name == "nt" else "clear")
print("\n----------------------------------")
print_green("Welcome to LinkedIn Auto Connect!")
print_yellow("Created by: klpod2211")
print("----------------------------------\n")
print_red("Note: Please read the following instructions carefully!")
print_red("1. Keyword is required! (e.g: Software Engineer)")
print_red(
    "2. Location keyword is optional!, if you don't want to add location, just press Enter"
)
print_red(
    "3. If you want to enter multiple location keywords, please separate them by comma (,) and no space (e.g: Ho Chi Minh City,Singapore)"
)
print_red("4. If you want to stop the program, just press Ctrl + C\n")
print("----------------------------------\n")

keyword = input("Enter keyword (required): ")
location_keyword = input("Enter location: ")

# check keyword and location keyword
if not keyword:
    print("Please enter keyword!")
    exit()

# check os and machine
path = "./drivers/"
if platform.system() == "Windows":
    if os.path.exists(path + "chromedriver.exe"):
        path += "chromedriver.exe"
    else:
        print("chromedriver.exe not found!")
        exit()
elif platform.system() == "Linux":
    if os.path.exists(path + "chromedriver"):
        path += "chromedriver"
    else:
        print("chromedriver not found!")
        exit()
elif platform.system() == "Darwin":
    if platform.machine() == "x86_64":
        if os.path.exists(path + "chromedriver"):
            path += "chromedriver"
        else:
            print("chromedriver not found!")
            exit()
    elif platform.machine() == "arm64":
        if os.path.exists(path + "chromedriver_arm64"):
            path += "chromedriver_arm64"
        else:
            print("chromedriver_arm64 not found!")
            exit()
    else:
        print("Unknown machine!")
        exit()
else:
    print("Unknown OS!")
    exit()

s = Service(path)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=s, options=options)


# Define functions
# function to check if element exists
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except:
        return False
    return True


# function to send connection request with note
def send_connection_request_with_note(name):
    # click Add a note
    driver.find_element(By.XPATH, '//button[@aria-label="Add a note"]').click()
    time.sleep(1)
    # type note
    textarea = driver.find_element(By.XPATH, '//textarea[@name="message"]')
    textarea.send_keys(
        "Hi "
        + name
        + ",\nI'm "
        + my_name
        + " from "
        + company_name
        + " - "
        + company_description
        + "\n. Nice to connect!"
    )
    # click Send now
    driver.find_element(By.XPATH, '//button[@aria-label="Send now"]').click()


# function to send connection request without note
def send_connection_request_without_note():
    # click Send now
    driver.find_element(By.XPATH, '//button[@aria-label="Send now"]').click()


# go to linkedin
driver.get("https://www.linkedin.com/login")
time.sleep(1)

# login
username = driver.find_element(By.ID, "username").send_keys(email)
password = driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH, '//button[@type="submit"]').click()

time.sleep(2)

# get current url
current_url = driver.current_url
# if current url is https://www.linkedin.com/checkpoint/...
if current_url.find("checkpoint") != -1:
    # wait for user to verify login
    print_red("Please verify your login!")
    while True:
        time.sleep(1)
        current_url = driver.current_url
        if current_url.find("feed") != -1:
            break

print_green("Login successfully!")

# find contact
keyword_parse = keyword.replace(" ", "%20")
driver.get(
    "https://www.linkedin.com/search/results/people/?keywords="
    + keyword_parse
    + "&origin=SWITCH_SEARCH_VERTICAL"
)

time.sleep(2)

# click to All Filters (aria-label="Show all filters. Clicking this button displays all available filter options.")
driver.find_element(
    By.XPATH,
    '//button[@aria-label="Show all filters. Clicking this button displays all available filter options."]',
).click()
time.sleep(1)

# find checkbox
driver.find_element(By.XPATH, '//label[@for="advanced-filter-network-S"]').click()
driver.find_element(By.XPATH, '//label[@for="advanced-filter-network-O"]').click()

# add location
# check location_keyword, if exists, add location
if location_keyword != "" and location_keyword != None:
    # split location_keyword by comma
    locations = location_keyword.split(",")

    # loop through locations
    for location in locations:
        driver.find_element(By.XPATH, '//button[span[text()="Add a location"]]').click()
        location_input = driver.find_element(
            By.XPATH, '//input[@placeholder="Add a location"]'
        )
        location_input.send_keys(location)

        location_input.send_keys("\ue015")
        time.sleep(1)
        location_input.send_keys("\ue015")
        time.sleep(1)
        location_input.send_keys("\ue007")
        time.sleep(1)

# click Show results
driver.find_element(
    By.XPATH, '//button[@aria-label="Apply current filters to show results"]'
).click()

time.sleep(2)

# get number of pages
# get artdeco-pagination artdeco-pagination--has-controls ember-view pv5 ph2
# pagination_wrapper = driver.find_element(
#     By.XPATH, '//div[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]'
# )
# last_page = pagination_wrapper.find_element(By.XPATH, "./li[last()]")
# last_page_number = last_page.get_attribute("data-test-pagination-page-btn")
last_page_number = "100"

if not os.path.exists("./connections"):
    os.mkdir("./connections")

# save to connections.csv
time_stamp = time.strftime("%Y%m%d-%H%M%S")
file_name = (
    keyword.replace(" ", "-")
    + "-"
    + location_keyword.replace(" ", "-").replace(",", "-")
    + "-"
    + time_stamp
    + ".csv"
)
file_name = file_name.lower()

for i in range(int(last_page_number)):
    current_url = driver.current_url
    current_url = current_url.split("&page=")[0] + "&page=" + str(i + 1)
    driver.get(current_url)
    time.sleep(2)

    all_buttons = driver.find_elements(By.XPATH, "//button")
    # find all connect buttons that have a span with text "Connect"
    connect_buttons = []
    for btn in all_buttons:
        try:
            if btn.find_element(By.XPATH, './span[text()="Connect"]'):
                connect_buttons.append(btn)
        except:
            pass

    time.sleep(2)

    for btn in connect_buttons:
        btn_aria_label = btn.get_attribute("aria-label")

        # Get user name
        user_name = btn_aria_label.split("Invite ")[1].split(" to connect")[0]

        # Get user url
        span = driver.find_element(By.XPATH, '//span[text()="' + user_name + '"]')
        parent = span.find_element(By.XPATH, "../..")
        user_url = parent.get_attribute("href").split("?")[0]

        # Click connect button
        btn.click()
        print("Inviting " + user_name + " to connect...")
        time.sleep(2)

        # check if is premium
        if send_with_note == "true":
            send_connection_request_with_note(user_name)
        else:
            send_connection_request_without_note()

        # write to file
        with open("./connections/" + file_name, "a") as f:
            f.write(user_name + "," + user_url + "\n")
        time.sleep(2)
