'''
This script scrapes the 500 paginated results of a query for
'slow cooker' recipes in the 'main dish' category. There are
supposed to be upwards of 600 pages, but the server must limit
the result set because pages past 500 (10,000 recipes) are empty.
The URLs of each individual recipe are collected for the single-page
crawler.
'''
from selenium import webdriver
import time
import pickle

chrome_path = "C:\Users\Jay\Desktop\Applied Data Science\project\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

recipe_urls = []
# Hard-code number of pages. The site lists extra blank pages for no reason..
numPages = 2
for pageNum in range(1, numPages):
    pageUrl = "https://www.bigoven.com/recipes/search/page/" + str(pageNum) + "?any_kw=slow+cooker&include_primarycat=Main+Dish"
    driver.get(pageUrl)
    time.sleep(5)
    # Extract recipe links from their panels in the grid layout
    html_list = driver.find_element_by_id("resultContainer")
    recipe_a_list = html_list.find_elements_by_css_selector(".panel-body > a:first-child")
    # iterate through web elements
    for j, e in enumerate(recipe_a_list):
        href = e.get_attribute("href")
        recipe_urls.append(href)

# Save the URL list to a pkl file
with open('pkls/recipe_urls.pkl', 'wb') as f:
    pickle.dump(recipe_urls, f)
