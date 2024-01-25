# Schokobon Coupon Importer

Python, Selenium Script to automatically activate coupon codes from the following [deal](https://www.mydealz.de/share-deal/2299297).

### Setup
- Download and install geckodriver for Firefox by following [the official selenium documentation](https://pypi.org/project/selenium/)
- Create python env: `python -m venv env`
- Activate env: `source env/bin/activate`
- Install requirements via pip: `pip install -r requirements.txt`

### Usage
- Create a .txt file containing one coupon code per line
- Run the script with the path to your code file and your email adress, example: `python -m main --file_path example_codes.txt --email foo@bar.de`
- You will receive your cinema tickets via mail

### Future Work
- Implement second script to automatically download tickets received via mail
