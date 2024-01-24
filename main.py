import time

from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.expected_conditions import \
    element_to_be_clickable


class CollectCoupons:
    def __init__(self, code_file_path, email) -> None:
        with open(code_file_path, 'r') as file:
            codes = file.readlines()

        opts = Options()
        #opts.add_argument("--headless")
        browser = Firefox(options=opts)
        browser.implicitly_wait(2)
        for code in [codes[12]]: #codes:
            code = code.strip()
            browser.get('https://www.kinder.com/de/de/xp/suchspass/#teilnehmen')

            cookies = browser.find_element(By.CSS_SELECTOR, '.ot-bnr-save-handler')
            if cookies is not None:
                cookies.click()
            #class ot-bnr-save-handler
                #.ot-bnr-save-handler
            #id=code
            #id=email
            code_input = browser.find_element(By.ID, 'code')
            code_input.send_keys(code)

            email_input = browser.find_element(By.ID, 'email')
            email_input.send_keys(email)

            email_input.submit()

            time.sleep(2)

            try:
                code_already_used = browser.find_element(By.CSS_SELECTOR, '[x-show="usedCode"]')
                if code_already_used.is_displayed():
                    print("code already used")
                    continue
            except:
                print("code not used")

            switch = browser.find_element(By.ID, 'switch-2')
            #ActionChains(browser).scroll_to_element(switch).click(switch).perform() #fix this
            browser.execute_script('arguments[0].scrollIntoView({ block: "center", inline: "center" });', switch)
            #element_to_be_clickable(switch)
            time.sleep(2)
            switch.click()
            switch.submit()
            time.sleep(10)
            #id switch-2
            #class="relative inline-block min-w-[240px] min-h-[80px] group focus:outline-0 disabled:hover:none"

class SaveCouponPdfs():
    def __init__(self) -> None:
        #empty
        pass

if __name__ == '__main__':
    CollectCoupons(code_file_path='codes.txt', email='sjonbon@jdeterding.de')
    SaveCouponPdfs()