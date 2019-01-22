# coding=utf-8

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import time
import random
import sys

start = time.time()
print("+++++++++++ AutoKMB v1.0 +++++++++++")

# FOR TESTING
# name = "Chan Tai Man"
# phone = "73541125"
# email = "ctm73541125@gmail.com"

name = "Liu Wai Lim"
phone = "92715426"
email = "14217643@life.hkbu.edu.hk"

if not (name and phone and email):
    print("***** Please input all fields to start AutoKMB *****")
    sys.exit()

counter = 0
tmpPoint = 0
tmpTicket = 0
failCount = 0

option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(chrome_options=option)

linkFile = open("link.txt", "r").read().splitlines()
random.shuffle(linkFile)

def keyIn():
    global counter
    if counter == 0:
        driver.find_element_by_id('mco_name').send_keys(name)
        driver.find_element_by_id('mco_phone').send_keys(phone)
        driver.find_element_by_id('mco_email').send_keys(email)
    else:
        pass
    driver.find_element_by_class_name('index_submit').click()

def result():
    global failCount, tmpPoint, tmpTicket
    try:
        if driver.find_element_by_class_name('submitted_points').text is not tmpPoint:
            tmpPoint = driver.find_element_by_class_name('submitted_points').text
        if "".join(filter(str.isdigit, driver.find_element_by_class_name("ticket_container").text)) is not tmpTicket:
            tmpTicket = "".join(filter(str.isdigit, driver.find_element_by_class_name("ticket_container").text))
        print(f"Points: {tmpPoint} / 20")
        if tmpTicket:
            print(f"Tickets: {tmpTicket}")
        else:
            print("Tickets: 0")
        log("[OK]")
    except NoSuchElementException:
        try:
            if driver.find_element_by_class_name('same_sticker_label').text:
                print("Invalid link, maybe expired/used")
                failCount = failCount + 1
        except NoSuchElementException:
            print("Unknown error")
            failCount = failCount + 1
        log("[FAIL]")

def log(text):
    print(text)
    print(text, file = open('result.txt', 'a'))

log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
log(f"Name: {name}")
log(f"Phone: {phone}")
log(f"Email: {email}")
log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

for link in linkFile:
    log(f">>>> {counter + 1} / {len(linkFile)} <<<<")
    driver.get(link)
    sleep(0.5)
    keyIn()
    sleep(1)
    counter = counter + 1
    result()
    if counter == len(linkFile):
        log("============= Result ==============")
        log(f"Clicked {len(linkFile)} links, {failCount} failed \n")
        if failCount != len(linkFile):
            log(f"Points: {tmpPoint} / 20")
            log(f"Tickets: {tmpTicket}")
        else:
            log("No points or tickets record can be retrieved")
        log("====================================")
    else:
        log("------------------------------------")

end = time.time()
log(f"Time used: {end - start} s")