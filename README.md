# Big Oven Recipe Scraping with Python [Spring 2017 Project]
This repository holds the scripts I am using to scrape (somewhat) standardized slow cooker recipes off of [Big Oven](https://www.bigoven.com/) using the selenium library. Big Oven has good HTML semantics to isolate each ingredient and quantity measurement as well as built in metric conversion, yield scaling and a calorie per serving approximation. 

The first script (big_oven_slow_cooker_urls.py) traverses the site's paginated collection of slow cooker recipes and grabs each of their URLs. In total, it gathers 10,000 URLs spread across 500 pages. The script takes 3-4 hours to finish.

The second script (big_oven_crawler.py) visits each recipe and extracts seven features; 
* url
* title
* rating
* number of reviews
* estimated prep time
* calories per serving
* ingredients (as a dictionary of name:quantity pairs)

A preliminary preprocessing step is achieved by adjusting Big Oven's built in recipe resizing inputs to convert measurements to metric and number of servings to 10 before extracting ingredients. 

Unfortunately, poorly authored recipes don't always behave properly, and additional post processing is needed. The base number of servings appears to be subjectively input which skews ingredient amounts. Due to bloated page-loading times and the key stroke steps, this script processes each recipe in 8-12 seconds. In 8 hours it can gather around 2,500 entries.
