import time

from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.expected_conditions import \
    element_to_be_clickable


class CollectCoupons:
    def __init__(self) -> None:
        codes = [
            "7XZPWFJRT2",
            "7XCE9YX247",
            "7X3RANWKZJ",
            "7XJX26LTM4",
            "7XTKWX4M6A"
        ]

        opts = Options()
        #opts.add_argument("--headless")
        browser = Firefox(options=opts)
        browser.implicitly_wait(10)
        for code in [codes[4]]: #codes:
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
            email_input.send_keys('sjonbon@jdeterding.de')

            email_input.submit()

            switch = browser.find_element(By.ID, 'switch-2')
            ActionChains(browser).scroll_to_element(switch).click(switch).perform() #fix this
            #element_to_be_clickable(switch)
            #switch.click()
            switch.submit()
            time.sleep(10)
            #id switch-2
            #class="relative inline-block min-w-[240px] min-h-[80px] group focus:outline-0 disabled:hover:none"

class SaveCouponPdfs():
    def __init__(self) -> None:
        #empty
        pass

if __name__ == '__main__':
    CollectCoupons()
    SaveCouponPdfs()