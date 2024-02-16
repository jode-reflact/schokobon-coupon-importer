# Schokobon Coupon Importer

Python, Selenium Script to automatically activate coupon codes from the following [deal](https://www.mydealz.de/share-deal/2299297).

### Setup
- Download and install geckodriver for Firefox by following [the official selenium documentation](https://pypi.org/project/selenium/)
- Install the requirements for textract by following [the official textract documentation](https://textract.readthedocs.io/en/stable/installation.html)
- Create python env: `python -m venv env`
- Activate env: `source env/bin/activate`
- Install requirements via pip: `pip install -r requirements.txt`

### Usage Coupon Collector
- Create a .txt file containing one coupon code per line
- Run the script with the path to your code file and your email adress, example: `python -m main --file_path example_codes.txt --email foo@bar.de`
- You will receive your cinema tickets via mail

### Usage PDF Coupon Saver
- Create an folder containing all coupon email files (.eml format)
- Create an empty folder for the outputed pdf's
- Run the script with the path to your input and output folders, example: `python -m save_pdf -i mail_input -o coupon_output --headless --skip_check_for_existing`
- It will also generate a excel file named "coupon_status.xlsx" which will include information about the coupon usage status

