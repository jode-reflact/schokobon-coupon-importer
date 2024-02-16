import argparse
import os
import time

import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


class CollectCoupons:
    def __init__(self, code_file_path: str, email: str, headless: bool) -> None:
        df_path = 'code_status.xlsx'
        
        if os.path.exists(df_path):
            df = pd.read_excel(df_path)
        else:
            df = pd.DataFrame(columns=['Code', 'Used', 'Downloaded'])

        with open(code_file_path, 'r') as file:
            codes = file.readlines()

        opts = Options()

        if headless:
            opts.add_argument("--headless")
        browser = Firefox(options=opts)
        browser.implicitly_wait(2)
        for code in codes:
            code = code.strip()
            #Check if code is already in df
            if len(df) > 0 and code in df['Code'].values:
                continue

            browser.refresh()
            browser.get('https://www.kinder.com/de/de/xp/suchspass/#teilnehmen')
            time.sleep(1)

            #Accept some cookies if needed
            try:
                cookies = browser.find_element(By.CSS_SELECTOR, '.ot-bnr-save-handler')
                if cookies.is_displayed():
                    cookies.click()
            except Exception as e:
                # Cookies already accepted
                cookies = None

            # Fill form and submit
            code_input = browser.find_element(By.ID, 'code')
            code_input.send_keys(code)

            email_input = browser.find_element(By.ID, 'email')
            email_input.send_keys(email)

            email_input.submit()

            time.sleep(2)

            # Checks if used was already used
            try:
                code_already_used = browser.find_element(By.CSS_SELECTOR, '[x-show="usedCode"]')
                if code_already_used.is_displayed():
                    print(f"Code {code} already used")
                    df.loc[len(df)] = [code, False, False] # Code, Used, Downloaded
                    df.to_excel(df_path, index=False)
                    continue
            except Exception as e:
                # Code not used
                code_already_used = None

            #Find "switch-2" which is the element with the correct answer
            switch = browser.find_element(By.ID, 'switch-2')

            #Scroll into view to enable click
            browser.execute_script('arguments[0].scrollIntoView({ block: "center", inline: "center" });', switch)
            time.sleep(2)

            #Click and Submit answer
            switch.click()
            switch.submit()

            #Saving used code to dataframe
            df.loc[len(df)] = [code, True, False] # Code, Used, Downloaded
            df.to_excel(df_path, index=False)

            #Cooldown time
            time.sleep(5)

        browser.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='Schokobon-Coupon-Collector')
    parser.add_argument('-f', '--file_path', type=str, required=True)
    parser.add_argument('-e', '--email', type=str, required=True)
    parser.add_argument('--headless', action='store_true') #Not tested yet

    args = parser.parse_args()

    CollectCoupons(code_file_path=args.file_path, email=args.email, headless=args.headless)