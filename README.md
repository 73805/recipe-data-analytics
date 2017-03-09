# Recipe Ingredient Associations
### Applied Data Science Project, Spring 2017

This project scrapes recipes from [Big Oven](https://www.bigoven.com/), processes the messy data down to a workable base table, and develops association rules based on a handful of features.

Data samples are available as pkl files or in a csv format (with ingredients converted from a python dictionary).

The recipe_url_aggregator gathers URLs for recipes from a paginated Big Oven search result. After aggregation, these URLs are used to direct recipe_url_crawler which visits individual recipes to extract a number of features including:
* title
* rating
* number of reviews
* estimated prep time
* calories per serving
* ingredients (as a dictionary of name:quantity pairs)

After collection, raw_recipe_processor cleans the data with various steps like dropping duplicates, converting to ascii, and removing implicit title words. The processed data is then passed to either of the unique ingredient scripts which further narrow the set and extract unique ingreidents. The quantified variant additionally collects associated units (cups, ml, cloves etc). The flattened variant simply collects un-quantified ingredient names.

Flattened ingredient names will be used to build ingredient association rules using (somewhat literal) market basket analyis.
