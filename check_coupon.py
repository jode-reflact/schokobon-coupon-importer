import argparse
import glob
import os
import time
import urllib.request
from typing import Optional

import pandas as pd
import regex
import textract
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


class CheckCoupon():
    def __init__(self, headless: bool) -> None:

        opts = Options()

        if headless:
            opts.add_argument("--headless")
        self.browser = Firefox(options=opts)
        self.browser.implicitly_wait(2)

        # url of the status checker
        self.url = 'https://portal.cadooz.com/portal/cinema/search.do'

        # regex to extract code and pin from pdf text string
        p = "(?<=CODE)(.*?)PIN.*BIS(.{8})"
        self.pattern = regex.compile(p, regex.S)
    
    # Future Work, not tested
    def check_all_coupons(self):
        df_path = 'coupon_status.xlsx'
        
        if not os.path.exists(df_path):
            print("Dataframe Path does not exist")
            quit()
        df = pd.read_excel(df_path)

        for idx, row in enumerate(df.rows):
            pdf_path = row['Path']
            code, pin = self.export_code_and_pin(pdf_path)
            used, text = self.check_single_coupon(code, pin)
            df.loc[idx] = [row['ID'], row['SUB'], pdf_path, used, text]

        df.to_excel(df_path, index=False)

    def export_code_and_pin(self, pdf_path: str):
        text = textract.process(pdf_path)
        text = ''.join(text.decode().splitlines())
        matches: list[tuple[str, str]] = self.pattern.findall(text)

        for code, pin in matches:
            code = code.replace(" ", "")
        return code, pin

    def close_browser(self):
        self.browser.close()

    def check_single_coupon(self, code: str, pin: str) -> (bool, str):
        self.browser.refresh()
        self.browser.get(self.url)
        time.sleep(1)

        #ID: code_id
        code_input = self.browser.find_element(By.ID, 'code_id')
        code_input.send_keys(code)

        #ID: pin_id
        pin_input = self.browser.find_element(By.ID, 'pin_id')
        pin_input.send_keys(pin)

        #onclick="checkVoucherCode
        btn = self.browser.find_element(By.CSS_SELECTOR, '[onclick^="checkVoucherCode"]')
        btn.click()

        time.sleep(5)

        #class redemption_status, row , col-xs-12 col-lg-12  success 
        detail_element = self.browser.find_element(By.CSS_SELECTOR, '.redemption_status > .row > .col-xs-12')
        text = detail_element.text

        used = False
        if "eingelöst" in text:
            used = True

        return used, text