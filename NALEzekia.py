#! /usr/bin/env python3

from selenium import webdriver
import time, os

browser = webdriver.Firefox()
browser.get('https://ezekia.com/#/login?redirect=%2Fassignments%2F16822%2Fcandidates')

browser.find_element_by_css_selector('.c-cookie-banner__btn').click()

emailElem = browser.find_element_by_name('email')
emailElem.send_keys('dan@ezekia.com')

#enter password
passwordElem = browser.find_element_by_css_selector('.o-form-login__inputs > div:nth-child(2) > input:nth-child(3)')
passwordElem.send_keys('Namchi51')
passwordElem.submit()

time.sleep(10)

#sort clients by date added
browser.find_element_by_css_selector('div.o-cand-panel__filter:nth-child(1)').click()
browser.find_element_by_css_selector('i.u-primary-color__text:nth-child(2)').click()
browser.find_element_by_css_selector('.c-basic-sorting__dropdown > div:nth-child(2) > div:nth-child(1) > div:nth-child(11) > div:nth-child(1)').click()

time.sleep(2)



#NEED TO FIND A WAY TO CYCLE THROUGH FILE LOCATION
rootdir ="/Users/danielharling/Desktop/CV's NAL"

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #click import on main page
        try:
            browser.find_element_by_css_selector('.o-cand-panel__import').click()
        except:
            pass
         
        if file == ".DS_Store" or file == "UserInfo.txt":
            continue
        pathName = os.path.join(subdir, file)
        #import desired CV
        browser.find_element_by_css_selector('.u-hidden').send_keys(pathName)
        time.sleep(8)

        #store date registered
        path = os.path.dirname(pathName)
        date = os.path.basename(path)

        try:
            #click notes
            notes = browser.find_element_by_css_selector('div.c-load-more__item:nth-child(1) > div:nth-child(1)')
            notes.find_element_by_xpath('.//*[@title="Notes"]').click()
        except Exception as e:
            print(e)
            continue
        time.sleep(1)

        #enter date registered
        try:
            browser.find_element_by_css_selector('.c-textarea__input').send_keys('Registered: ' + date)
        except:
            browser.find_element_by_css_selector('.c-create__icon').click()
            browser.find_element_by_css_selector('.c-textarea__input').send_keys('Registered: ' + date)

        #Delete CV once uploaded, delet folder if empty
        os.remove(pathName)
        time.sleep(3)
        try:
            os.rmdir(subdir)
        except:
            pass        
               
        time.sleep(1)
        #click save
        browser.find_element_by_css_selector('span.c-save-cancel__button:nth-child(2)').click()
        time.sleep(4)
        #click exit
        browser.find_element_by_css_selector('.fa-times').click()
        time.sleep(5)
