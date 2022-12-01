from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

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

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# driver.get('http://nytimes.com')
# print(driver.title)

from jd_crawler import jd_crawler
import pandas as pd

jd = jd_crawler(driver)
with open('jd_list.txt', 'r') as f:
    jd_list = f.readlines()

results = jd.query_skus(jd_list)

df = pd.DataFrame.from_records(results)
df.to_csv('jd_results.csv', float_format='%.2f', index=False, encoding='utf-8-sig')