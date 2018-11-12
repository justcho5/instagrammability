# open page
# once page is loaded, click the user
# Extract the number of followers, photo link
# close browser

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html

import csv

def write_out_csv(data, filename_base, fieldnames):
    print("Writing to output file %s.csv" % filename_base)
    with open('%s.csv' % filename_base, 'w') as csvfile:
        fields = fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 15)

with open('elysee_shortcode.csv', 'r') as f:
    reader = csv.reader(f)
    codes = [code[0] for code in list(reader)]

# codes = ["BQuo1jphe_a"]
instagram_data = []
for code in codes:
    url = "https://instagram.com/p/"+code
    browser.get(url)
    elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "e1e1d"]//a[@class = "FPmhX notranslate nJAzx"]')))

    elem.click()
    elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "v9tJq "]')))
    el = browser.find_element_by_xpath("//*")
    parser = html.fromstring(el.get_attribute("outerHTML"))
    # print(el.get_attribute("outerHTML"))
    raw_followers = parser.xpath(
        './/ul[@class="k9GMp "]/li[position()=2]//span[@class = "g47SY "]/@title')[0].replace(",", "")

    data = {
        "shortcode": code,
        "followers": int(raw_followers),
    }
    print(data)

    instagram_data.append(data)
browser.close()
fields = ['shortcode', 'followers']
write_out_csv(instagram_data, "followers", fields)

