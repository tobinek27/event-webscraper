#!/usr/bin/python3
from discord import SyncWebhook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import yaml
import datetime


webhook = SyncWebhook.from_url('<unique_webhook_url>')
cfg = yaml.safe_load(open('login_details.yml')) # load login details
my_username = cfg['account']['username'] # username
my_password = cfg['account']['password'] # password
driver_options = webdriver.ChromeOptions() # choose chrome webdriver
driver_options.add_argument("--headless") # run headless
#driver_options.add_argument("--no-sandbox")
#driver_options.add_argument("--disable-dev-shm-using")
#driver_options.add_argument("--disable-extensions")
#driver_options.add_argument("--disable-setuid-sandbox")
#driver_options.add_argument("--remote-debugging-port=9222")
#driver_options.add_argument("--disable-gpu")
#driver_options.add_argument("start-maximized")
#driver_options.add_argument("disable-infobars")
driver = webdriver.Chrome(options=driver_options, service=Service(ChromeDriverManager().install())) # update chrome webdriver


# log-in at a specified website
def login(url:str):
    '''
    login function logs the user in

    :param url: url address of spsejecna
    '''
    driver.get(url)

    website_username = driver.find_element(By.XPATH, "//input[@tabindex='1']")
    website_password = driver.find_element(By.XPATH, "//input[@tabindex='2']")
    website_button = driver.find_element(By.XPATH, "//input[@tabindex='3']")

    website_username.send_keys(my_username)
    website_password.send_keys(my_password)
    website_button.click()


def check_for_new_post():
    '''
    logs in and checks for latest 'event' post
    '''

    login('https://spsejecna.cz/user/role?role=student')
    driver.get('https://spsejecna.cz/akce/')
    wait = WebDriverWait(driver, 10)
    event_contents = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'event'))).text
    return event_contents


newest_website_post = check_for_new_post()

# check the 'latest_event.txt' file to confirm if event is new or not changed

file1 = open('latest_event.txt', 'r', encoding='utf-8')
file1_readlines = file1.readlines()
file1_contents = ''
for i in file1_readlines: # convert the list of lines to string
    file1_contents += i

if newest_website_post != file1_contents:
    file2 = open('/home/tobinek/jecna_news/latest_event.txt', 'w', encoding='utf-8')
    file2.write('{}'.format(newest_website_post)) # overwrites the 'latest_event.txt' file's content
    webhook.send('@everyone cs\r\n{}'.format(newest_website_post)) # posts the new event via the Discord webhook