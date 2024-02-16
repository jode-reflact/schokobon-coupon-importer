import argparse
import glob
import os
import time
import urllib.request
from typing import Optional

import pandas as pd
import regex
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from check_coupon import CheckCoupon


class SaveCouponPdfs():
    def __init__(self, input_folder: str, output_folder: str, headless: bool, skip_check_for_existing: bool) -> None:
        coupon_checker = CheckCoupon(headless)

        if not os.path.exists(input_folder):
            print("Input Path not found, aborting")
            quit()
        input_folder = os.path.abspath(input_folder)

        if not os.path.exists(output_folder):
            print("Output Path not found, aborting")
            quit()
        output_folder = os.path.abspath(output_folder)
        
        df_path = 'coupon_status.xlsx'
        
        if os.path.exists(df_path):
            df = pd.read_excel(df_path)
        else:
            df = pd.DataFrame(columns=['ID', 'SUB', 'Path', 'Used', 'Used_Details'])

        # find all .eml files in input folder
        mail_files = glob.glob(f"{input_folder}/**/*.eml", recursive=True)

        # regex to extract href id and sub for coupon download
        p = "(?<=>https:\/\/ecard\.cadooz\.com\/frontend\/ecard\.do\?id=3D)(.*?)sub\=3D(.*?)(?=c\=)"
        pattern = regex.compile(p, regex.S)

        opts = Options()

        if headless:
            opts.add_argument("--headless")
        browser = Firefox(options=opts)
        browser.implicitly_wait(2)

        for mail_file in mail_files:
            with open(mail_file, "r") as file:
                mail_content = file.read()
            mail_content = ''.join(mail_content.splitlines())
            mail_content = mail_content.replace("&amp;", "")

            #should always be 1 match
            matches: list[tuple[str, str]] = pattern.findall(mail_content)

            for coupon_id, sub in matches:
                # replace "=" characters which get generated on line breaks
                coupon_id = coupon_id.replace("=", "")
                sub = sub.replace("=", "")
                print(coupon_id, sub)

            # check whether df already contains this coupon
            index_list = df[(df['ID'] == f"{coupon_id}")&(df['SUB'] == f"{sub}")].index.tolist()

            # if coupon is not known, download pdf
            if len(index_list) == 0:
                url = f"https://ecard.cadooz.com/frontend/ecard.do?id={coupon_id}&sub={sub}"

                browser.refresh()
                browser.get(url)
                time.sleep(1)

                pdf_url: Optional[str] = None

                link_button = browser.find_element(By.CSS_SELECTOR, '[title="Hier PDF anzeigen."]')
                pdf_url = link_button.get_attribute('href')

                print("pdf_url", pdf_url)

                entry_idx = len(df)

                if pdf_url is not None:
                    pdf_path = f"{output_folder}/{coupon_id}_{sub}.pdf"
                    urllib.request.urlretrieve(pdf_url, pdf_path)
                else:
                    print("Abort, unkown error")
                    quit()
            else:
                entry_idx = index_list[0]
                entry = df.loc[entry_idx]
                pdf_path = entry['Path']
                print(f"skipped {pdf_path}")
                if skip_check_for_existing:
                    continue

            # export coupon code and pin from pdf to check status
            code, pin = coupon_checker.export_code_and_pin(pdf_path)

            # checking coupon status and saving detail text
            used, used_details = coupon_checker.check_single_coupon(code, pin)

                                 #['ID', 'SUB', 'Path', 'Used', 'Used_Details']
            df.loc[entry_idx] = [coupon_id, sub, pdf_path, used, used_details]
            df.to_excel(df_path, index=False)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Coupon-Saver')
    parser.add_argument('-i', '--input_folder', type=str, required=True)
    parser.add_argument('-o', '--output_folder', type=str, required=True)
    parser.add_argument('--headless', action='store_true')

    parser.add_argument('-skip','--skip_check_for_existing', action='store_true', default=False, help="Whether to skip the status check for known coupons")

    args = parser.parse_args()

    SaveCouponPdfs(input_folder=args.input_folder, output_folder=args.output_folder, headless=args.headless, skip_check_for_existing=args.skip_check_for_existing)