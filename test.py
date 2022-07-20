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

    def wait_click_element(self,xpath):

        en_btn = self.browser.find_element(By.XPATH,xpath)
        print('1')
        ActionChains(self.browser).move_to_element(en_btn).perform()
        print('2')
        WebDriverWait(self.browser, 20).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
        return en_btn

    def visit_targets_a(self):

        # for url in self.targets_a.keys():
        try:
            # self.browser.switch_to.new_window('tab')
            self.browser.get('https://seller.shopee.com.my/portal/product/list/all')
            time.sleep(20)

        except Exception as e:
            print('url loading failed!!')

        # do some automation stuff
        loginBtnXpath = '//*[@id="shop-login"]/div[4]/div/div/button'
        loginBtn = self.wait_click_element(loginBtnXpath)
        emailInput = self.browser.find_elements(By.CLASS_NAME, 'shopee-input__input')[0]
        emailInput.send_keys('kiman.ma@yahoo.com')
        time.sleep(1)
        passInput = self.browser.find_elements(By.CLASS_NAME, 'shopee-input__input')[1]
        passInput.send_keys('Jaibrutal1970')
        loginBtn.click()
        time.sleep(2)

        print('All done!')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.browser.quit()

spider = ItsyBitsy(teardown=True)
spider.visit_targets_a()