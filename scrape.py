import sys, json, lxml.html
import html as py_html
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

with open('config.json', 'r') as f:
    config = json.load(f)

# Chrome and phantomJS driver paths
path_to_chromedriver = './drivers/chromedriver'
path_to_phantomjs = '/usr/bin/phantomjs'

if (len(sys.argv) > 1 and sys.argv[1] == '--chrome'):
    browser = webdriver.Chrome(path_to_chromedriver)
else:
    browser = webdriver.PhantomJS(path_to_phantomjs)


# Login
print("Logging in")
base_url = 'https://practiceit.cs.washington.edu'
browser.get(base_url + '/login')
username = browser.find_element_by_id('usernameoremail')
password = browser.find_element_by_id('userpassword')
username.clear()
password.clear()
username.send_keys(config['user']['name'])
password.send_keys(config['user']['password'])
browser.find_element_by_id('submitbutton').click()
print("Logged in")

# Nav to the problems page
browser.get(base_url + '/problem/list')

# Parse the categories
print("Scraping category list")
category_path = '//*[@id="categories"]/h4'
categories = list(browser.find_elements_by_xpath(category_path))
category_html = {}
print(str(len(categories)) + " categories found: ")
for i,cat in enumerate(categories):
    print('\t[' + str(i) + ']: '+ cat.text.split('\n')[0])
    cat_list = cat.find_element_by_xpath('following-sibling::*')
    category_html[i] = lxml.html.fromstring(cat_list.get_attribute('innerHTML'))
    category_html[i].make_links_absolute(base_url)

# Prompt user for category selection
input_numbers = input("Enter desired category numbers, seperated by spaces. (Leave blank for all): ")
input_numbers = list(map(lambda x: int(x), input_numbers.split()))
if len(input_numbers) == 0:
    input_numbers = range(0, len(categories))

# Parse code solutions, print to stdout
for i in input_numbers:
    print("Scraping category " + str(i))
    html = category_html[i]
    for prob in html.find_class("problemlink"):
        href = prob.get('href')
        browser.get(href)
        print(href.split('/').pop())
        try:
            # could make this a randomized wait if we feel like Stuart Reges
            # is on to us
            time.sleep(2)
            solution = browser.find_element_by_id("solution")
            soln_text = str(py_html.unescape(solution.get_attribute('innerHTML')))
            print(soln_text)
            file_name = str(href.split('/').pop())
            print("Writing file")
            f = open(file_name, 'w')
            f.write(soln_text)
            f.close()
        except:
            print("No code solution found")
        print()
        browser.back()
    
print("Done scraping")
