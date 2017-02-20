from selenium import webdriver
import time
import pandas as pd

chrome_path = "C:\Users\Jay\Desktop\Applied Data Science\project\chromedriver.exe" 
driver = webdriver.Chrome(chrome_path)

recipe_urls = []
# Hard-code number of pages. The site lists extra blank pages for no reason..
numPages = 500
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
        print href

# Convert list to dataframe and export to csv
df = pd.DataFrame(recipe_urls)
df.to_csv('big_oven_slow_cooker_urls.csv', header='urls')
