import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

chrome_path = r'C:\Users\Jay\Desktop\Applied Data Science\project\chromedriver.exe'

# Get adblock extension working
ad_block_path = r'C:\Users\Jay\Desktop\Applied Data Science\project\1.11.0_0'
chrome_options = Options()
chrome_options.add_argument('load-extension=' + ad_block_path)

# Get the list of 10,000 URLS
urls = pd.read_csv("csvs/big_oven_slow_cooker_urls.csv")
urls = list(urls['urls'])

# initiate main Data Frame
column_headers = ["url", "title", "stars", "reviews", "prep_time", "calories_per_serving", "ingredients_flat", "flag"]
big_data = pd.DataFrame(columns=column_headers)

start_place = 499
new_window = True

for j in range(start_place, 10000):
    # get the current URL
    url = urls[j]
    
    # Open a new window if needed
    if new_window:
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.create_options()
    driver.get(url)

    # Extract Title
    title = driver.find_element_by_css_selector("h1.fn").text

    # Extract Rating information (sometimes unlisted)
    try:
        ratingHandle = driver.find_element_by_id("rc")
        # Get the hidden rating value
        ratingInner = ratingHandle.get_attribute("innerHTML")
        # access substring with number in it
        r = ratingInner.split(">")
        stars = float(r[-2][:-6])
        reviews = driver.find_element_by_css_selector("#rc .count").text
        # trim 'reviews' from end of string
        reviews = int(reviews[:-7])
    except NoSuchElementException:
        stars = "NA"
        reviews = "NA"

    # Extrat Preparaton time (trim string)
    prep_time = driver.find_element_by_css_selector(".duration time").get_attribute("title")
    prep_time = prep_time[2:-1]

    # Extracting ingredients with some preliminary steps
    # Set ignredient measurements to Metric
    driver.find_element_by_xpath('//*[@id="resizeForm"]/div/div/button').click()
    time.sleep(1)
    driver.find_element_by_css_selector(".servingSize .btn-group .dropdown-menu li:last-child").click()
    time.sleep(1)
    # Set Servings to 10
    servings = driver.find_element_by_xpath('//*[@id="resizeForm"]/span[1]/input')
    servings.send_keys(Keys.BACKSPACE)
    servings.send_keys(Keys.BACKSPACE)
    servings.send_keys('10')
    servings.send_keys(Keys.RETURN)
    time.sleep(1)
    
    # Get the ingredients and package them in a dictionary "name" : "amount"
    ingredients = {}
    amount = ""
    name = ""
    ingred_list = driver.find_elements_by_css_selector(".ingredientbox .ingredient")
    flag = 0
    for i, ingred in enumerate(ingred_list):
        try:
            name = ingred.find_element_by_css_selector(".name .glosslink").text
        except NoSuchElementException:
            name = ingred.find_element_by_css_selector(".name").text
            # Count glosslink failures
            flag = flag + 1
        try:
            amount = ingred.find_element_by_css_selector(".amount").text
        except NoSuchElementException:
            amount = ""

        ingredients[name] = amount

    # Extract Calories per serving from nutrition tab
    driver.find_element_by_css_selector("a[href*='#nutrition']").click()
    time.sleep(1)
    try:
        calories_per_serving = driver.find_element_by_css_selector("#tab-nutrition p > span").text
    except NoSuchElementException:
        calories_per_serving = "NA"
  
    # Create an array of the extracted features
    new_row = [url, title, stars, reviews, prep_time, calories_per_serving, ingredients, flag]
    # Add new row to data frame
    big_data.loc[j] = new_row
    
    # Re-open browser window every 100 recipes (helps with memory dumping)
    if (j + 1 - start_place) % 100 == 0:
        new_window = True
        driver.quit()
    else:
        new_window = False
        
    # print the index for sanity / progress checks
    print j

# pickle the data frame
fn = "glosslinked_data_" + str(start_place) + "_" + str(j - 1) + ".pkl"
big_data.to_pickle(fn)

#big_data.to_csv(fn, header=column_headers, encoding='utf-8')
