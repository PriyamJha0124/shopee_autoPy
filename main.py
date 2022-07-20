from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import os
class ItsyBitsy(object):
    def __init__(self, teardown=False):
        self.teardown = teardown
        self.targets_a = dict({'https://seller.shopee.com.my/portal/product/list/all':'product_list'}) # data like url:document_summary 

        profile_dir = os.path.join(os.getcwd(),'shopee')
        print(profile_dir)
        if not os.path.exists(profile_dir):
            os.mkdir(profile_dir)
            print("Directory " , profile_dir ,  " Created ")
        else:    
            print("Directory " , profile_dir ,  " already exists")

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("user-data-dir={}".format(profile_dir)) #Path to your chrome profile
        options.add_argument('--profile-directory=profile')
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        self.browser.set_page_load_timeout(60)

    def wait_click_element(self,xpath):

        en_btn = self.browser.find_element(By.XPATH,xpath)
        print('1')
        ActionChains(self.browser).move_to_element(en_btn).perform()
        print('2')
        WebDriverWait(self.browser, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
        return en_btn

    def visit_targets_a(self):
        print('start')
        # for url in self.targets_a.keys():
        try:
            self.browser.get('https://seller.shopee.com.my/portal/product/list/all')
            print("step-1")
        except:
            cu785=self.browser.current_url
        print("page loaded")
        # self.browser.set_page_load_timeout(60)
        repeat = True
        while repeat:
            time.sleep(10)
            # do some automation stuff
            print('middle')
            try:
                loginBtnXpath = '//*[@id="shop-login"]/div[4]/div/div/button'
                loginBtn = self.wait_click_element(loginBtnXpath)
                emailInput = self.browser.find_elements(By.CLASS_NAME, 'shopee-input__input')[0]
                emailInput.send_keys('xxxxxxxxxxxxxxx')
                time.sleep(1)
                passInput = self.browser.find_elements(By.CLASS_NAME, 'shopee-input__input')[1]
                passInput.send_keys('yyyyyyyyyyyyyy')
                loginBtn.click()
                time.sleep(5)
                try:
                    enXpath = '//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button'
                    enBtn = self.wait_click_element(enXpath)
                    enBtn.click()
                    print('clicked_languageBtn')
                except:
                    pass
                time.sleep(2)
                verifyXpath = '//*[@id="main"]/div/div[2]/div/div/div/div[1]/div/div[2]/div/button'
                verifyBtn = self.wait_click_element(verifyXpath)
                verifyBtn.click()
                print('clicked_VerifyBtn')
                time.sleep(3)
                verify2Xpath = '//*[@id="modal"]/aside/div[1]/div/div[2]/button[2]'
                verify2Btn = self.wait_click_element(verify2Xpath)
                verify2Btn.click()
                time.sleep(10)
            except Exception as e:
                print('error:',e)
                pass
            try:
                moreBtns = self.browser.find_elements(By.CLASS_NAME, 'more-dropdown')
                prodLen = len(moreBtns)
                bumpBtns = self.browser.find_elements(By.CLASS_NAME, "boost-button-text")
                print(prodLen)
                bosted = 0
                if len(moreBtns)>0:
                    repeat = False
                    for moreBtn in moreBtns:
                        try:
                            moreBtn.click()
                            time.sleep(1)
                            for bumpBtn in bumpBtns:
                                try:
                                    bumpBtn.click()
                                    time.sleep(1)
                                    print('bosted!')
                                    bosted = bosted + 1
                                except:
                                    pass
                            moreBtn.click()
                            time.sleep(1)
                        except Exception as e:
                            print(e)
                    # if bosted < 1:
                    leftTimes = []
                    try:
                        timeCountings = self.browser.find_elements(By.CLASS_NAME, 'count-cool')
                        for timeCount in timeCountings:
                            elems = timeCount.get_attribute("innerHTML").replace('\n','').replace(' ','').split(":")
                            secs = int(elems[0]) * 3600 + int(elems[1]) * 60 + int(elems[2])
                            leftTimes.append(secs)
                            leftTimes.sort()
                        waitSec = leftTimes[0]
                    except:
                        waitSec = 7200
            except:
                pass
        try:
            return waitSec
        except:
            return int(7200)


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.browser.quit()

spider = ItsyBitsy(teardown=True)
while True:
    waitTime = spider.visit_targets_a()
    print(waitTime)
    time.sleep(waitTime)