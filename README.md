# Big Oven Recipe Scraping with Python
This repository holds the scripts I am using to scrape (somewhat) standardized slow cooker recipes off of [Big Oven](https://www.bigoven.com/) using the selenium library.

The first script visits the paginated collection of links to recipes to gather 10,000 URLs and takes 3-4 hours to complete (each page displays 20 recipes in a grid.

The second script extracts seven features of each recipe including a dictionary of ingredients and their amounts. This script accesses Big Oven's built in recipe resizing inputs to convert measurements to metric and number of servings to 10 before extracting ingredients. The scraped data still requires processing due to mis-typed quantities and the apparently subjective nature of the base 'servings' count. (ex: a range of 2-3 pounds is converted to nothing, and the author of the recipe can specify how many servings it makes). 
