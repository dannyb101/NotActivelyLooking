#find table containing info
#table = browser.find_element_by_css_selector('.table > tbody:nth-child(2)')
#table.find_element_by_css_selector

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


import os.path
from os import path
import time, random


#set download prefereneces
profile = webdriver.FirefoxProfile() 
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/msword, application/octet-stream, application/x-winzip, application/x-pdf, application/x-gzip")
profile.set_preference("pdfjs.disabled", True)
profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/msword,application/octet-stream, application/x-winzip, application/x-pdf, application/x-gzip")

def set_download_dir(driver, directory):
  driver.command_executor._commands["SET_CONTEXT"] = ("POST", "/session/$sessionId/moz/context")
  driver.execute("SET_CONTEXT", {"context": "chrome"})

  driver.execute_script("""
    Services.prefs.setBoolPref('browser.download.useDownloadDir', true);
    Services.prefs.setStringPref('browser.download.dir', arguments[0]);
    """, directory)

  driver.execute("SET_CONTEXT", {"context": "content"})

def printTime(time):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return time + dt_string

def writeUserInfo(info):
    infoFile = open("/Users/danielharling/Desktop/NAL/UserInfo/UserInfo.txt","a+")
    infoFile.write(info + '\n')
    infoFile.close()

writeUserInfo(printTime('Start: '))

#open webbrowser and navigate to NAL
browser = webdriver.Firefox(firefox_profile=profile)
browser.get('http://notactivelylooking.com/nova')

#enter email
emailElem = browser.find_element_by_id('email')
emailElem.send_keys('dan@notactivelylooking.com')

#enter password
passwordElem = browser.find_element_by_id('password')
####Password removed #####
passwordElem.submit()

#Wait for authentication
input('Press enter once authentication has been entered...')

#click premium users
browser.find_element_by_css_selector('ul.list-reset:nth-child(7) > li:nth-child(1) > a:nth-child(1)').click()


time.sleep(10)
#Click registered to orderfrom oldest to newest
browser.find_element_by_css_selector('th.text-left:nth-child(6) > span:nth-child(1)').click()


#navigate to page 
page = input('Please enter required page number:\n')
browser.get('https://notactivelylooking.com/nova/resources/executives?executives_page=' + page + \
            '&executives_order=created_at&executives_direction=asc')


while True:
    newpage = input('Is the page number correct?\nIf not enter the new number:')
    if newpage =='':
        break
    browser.get('https://notactivelylooking.com/nova/resources/executives?executives_page=' + newpage + \
            '&executives_order=created_at&executives_direction=asc')


noPages = int(input('How many pages would you like to evaluate?\n'))

for i in range(noPages):
    for i in range(1,26):
    
        if i ==1:
            time.sleep(6)
        
        
        
        rowcss = browser.find_element_by_css_selector('.table > tbody:nth-child(2) > tr:nth-child(' + str(i) +')')

        #Save date registered in date variable
        date = browser.find_element_by_css_selector('.table > tbody:nth-child(2) > tr:nth-child(' + str(i) +\
                                                    ') > td:nth-child(6) > div:nth-child(1) > span:nth-child(1)').text
    
        #save name
        name = browser.find_element_by_css_selector('.table > tbody:nth-child(2) > tr:nth-child(' + str(i) +\
                                                    ') > td:nth-child(4) > div:nth-child(1) > span:nth-child(1)').text
    

        #See if active premium
        try:
            rowcss.find_element_by_css_selector('.text-success')
        except:
            
            continue
    
        time.sleep(random.randint(0,3))

        try:
            #click impersonate
            #NEED TO SCROLL TO SEE ELEMENT?
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', '.overflow-hidden')        
            impersonate = browser.find_element_by_css_selector('.table > tbody:nth-child(2) > tr:nth-child(' + str(i) + ') > td:nth-child(10) > a:nth-child(1) > svg:nth-child(1) > path:nth-child(1)')
            impersonate.click()
                 
        except Exception as e:
            print(e)
            print('Failed at impersonate for user ' + name)
            continue
    
        try:
            #click cookie banner
            try:
                browser.find_element_by_css_selector('.c-cookie-banner__btn').click()
            except:
                pass
            time.sleep(5)

            userProfile = browser.find_element_by_xpath('/html/body/div[1]/div[5]/div/div/div[2]/div[1]/div/div[1]/div[3]/span/a[1]/i')
            userProfile.click()


            dateFile = "/Users/danielharling/Desktop/CV's NAL/" + date
            #check if directory exists, if not create
            if not os.path.exists(dateFile):
                os.makedirs(dateFile)
            else:
                pass

            set_download_dir(browser, dateFile)

            #download cv or all files available
            cv = browser.find_element_by_css_selector('.o-profile-documents__documents')
            docs = cv.find_elements_by_tag_name('a')

            #If multiple files write to file so as to check later
            if len(docs) > 1:
              multiFile = 'Multiple files downloaded for: ' + name + ' Registered: ' + date
              print(multiFile)
              writeUserInfo(multiFile)
            for x in docs:
                x.click()
                time.sleep(4)

            cvSuccess = name + " registerd " + date + ' - cv download successful!'
            writeUserInfo(cvSuccess)
            print(cvSuccess)
     
            #reverse impersonate
            reverse = browser.find_element_by_xpath('/html/body/div[2]/a')
            reverse.click()
            time.sleep(10)
                                                                   
        except Exception as e:
            print(e)
            LinkedInReq = 'NO CV FOR: ' + name + ' Registered: ' + date
            writeUserInfo(LinkedInReq)
            print(LinkedInReq)
          
            reverse = browser.find_element_by_xpath('/html/body/div[2]/a')
            reverse.click()
            time.sleep(10)

    #click to next page
    browser.find_element_by_css_selector('button.btn:nth-child(3)').click()
        
writeUserInfo(printTime('End: '))
          
                                        

    
    




        





                            
