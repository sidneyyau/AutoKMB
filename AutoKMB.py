# coding=utf-8

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import time
import random
import re

print("+++++++++++ AutoKMB v2.0 +++++++++++")

while True:
    print("* Please input all fields to start AutoKMB *")
    name = input("Name: ")
    phone = input("Phone no.: ")
    email = input("Email address: ")
    if name and phone and email:
        break

counter = 0
tmpPoint = 0
tmpTicket = 0
failCount = 0
failedLink = ['']

mobileEmulation = {
    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36" }
option = webdriver.ChromeOptions()
option.add_argument('headless')
# option.add_argument('window-size=1920x1080')
option.add_experimental_option("mobileEmulation", mobileEmulation)
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

def result(url):
    global tmpPoint, tmpTicket, failCount
    currentURL = driver.current_url
    while "time" in currentURL:
        currentURL = driver.current_url
    if "same_sticker_error" in currentURL:
        print("Used link")
        log("[FAIL]")
        failedLink.append(url)
        failCount = failCount + 1
    else:
        tmpPoint = re.findall('(?<=new_pts=)\d\d?', currentURL)[0]
        tmpTicket = re.findall('(?<=ticket=)\d\d?\d?', currentURL)[0]
        print(f"Points: {tmpPoint} / 20")
        print(f"Tickets: {tmpTicket}")
        log("[OK]")

def log(text):
    print(text)
    print(text, file = open('result.txt', 'a'))

start = time.time()
log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
log(f"Name: {name}")
log(f"Phone: {phone}")
log(f"Email: {email}")
log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

for link in linkFile:
    log(f">>>> {counter + 1} / {len(linkFile)} <<<<")
    driver.get(link)
    sleep(0.3)
    keyIn()
    counter = counter + 1
    result(link)
    if counter == len(linkFile):
        log("============= Result ==============")
        log(f"Clicked {len(linkFile)} links, {failCount} failed \n")
        if failCount != len(linkFile):
            log(f"Points: {tmpPoint} / 20")
            log(f"Tickets: {tmpTicket}")
            if len(failedLink) > 0:
                print("\nList of failed links:")
                for fLink in failedLink:
                    print(fLink)
        else:
            log("No points or tickets record can be retrieved")
        log("====================================")
    else:
        log("------------------------------------")

driver.close()
end = time.time()
log(f"Time used: {end - start} s")