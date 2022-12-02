from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType #, read_version_from_cmd, PATTERN
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

if "GITHUB_ACTION" in os.environ: 
    # version = read_version_from_cmd("/usr/bin/chromium-browser --version", PATTERN[ChromeType.CHROMIUM])
    # chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, version=version, path='/usr/bin/chromium-browser') .install())
    # chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, path='/usr/bin/chromium-browser') .install())\
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM) .install())
else:
    chrome_service = Service(ChromeDriverManager().install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

chrome_options.experimental_options["prefs"] = {
    "profile.default_content_settings": {"images": 2},
    "profile.managed_default_content_settings" : {"images": 2},
    
}
chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# driver.get('http://nytimes.com')
# print(driver.title)

from jd_crawler import jd_crawler
# import pandas as pd

jd = jd_crawler(driver)
with open('jd_list.txt', 'r') as f:
    jd_list = f.readlines()

results = jd.query_skus(jd_list)

# df = pd.DataFrame.from_records(results)
# df.to_csv('jd_results.csv', float_format='%.2f', index=False, encoding='utf-8-sig')
from csv import DictWriter
with open("results/jd_results.csv", 'a', encoding='utf-8-sig') as csv_file:
    writer_object = DictWriter(csv_file, fieldnames=results[0].keys())
    writer_object.writerows(results) 
