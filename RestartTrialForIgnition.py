from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-hs",
    "--host",
    help="Ignition Gateway Host",
    type=str,
    default="http://localhost:8088/",
)
parser.add_argument(
    "-u", "--username", help="Gateway Username", type=str, default="admin"
)
parser.add_argument(
    "-p", "--password", help="Gateway Password", type=str, default="password"
)
parser.add_argument("-s", "--silent", help="No Browser", action="store_true")

args = parser.parse_args()

username = args.username
password = args.password
gateway_url = args.host

# "http://bctjakned.local:8088/"

# 3 scenarios:
# - Trial is still running
# - Trial is out and you need to log in
# - Trial is out and you are already logged in

options = Options()

if args.silent:
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

trial_expired = True

# Initiate browser
browser = webdriver.Chrome(options=options)

# Navigate to the site
browser.get(gateway_url)

# Wait for the page to load
sleep(1)

# Try locating the reset trial button element. If not found then trial is still running
try:
    # Click "sign in to reset trial" button
    browser.find_element(By.ID, "reset-trial-anchor").click()
    sleep(1)

except NoSuchElementException:
    trial_expired = False
    remaining_time = browser.find_element_by_class_name("countdown").text
    print("Trial is not expired, {} remaining".format(remaining_time))

if trial_expired:
    try:
        # Fill in username
        usr_element = browser.find_element_by_name("username")
        usr_element.send_keys(username)

        # Click next
        browser.find_element_by_class_name("submit-button").click()

        # Fill in password
        pw_element = browser.find_element_by_name("password")
        pw_element.send_keys(password)

        # Click next
        browser.find_element_by_class_name("submit-button").click()

        sleep(1)

        # Click "sign in to reset trial" button
        browser.find_element(By.ID, "reset-trial-anchor").click()

        print("Trial Restarted")

    except NoSuchElementException:
        print("Already Logged in, Trial Restarted")

sleep(3)
browser.quit()
