import pandas as pd
import ast
import re

'''
from pymongo import MongoClient
client = MongoClient()
db = client.rdb
'''

df = pd.read_csv("csvs/base_table_FULL_rawish.csv")

# Define some regular expressions
sc_strip = re.compile(r'slow[-|\s]?cooke[r|d]\s?', re.IGNORECASE)
cp_strip = re.compile(r'crock[-|\s]?pot\s?', re.IGNORECASE)
rcp_strip = re.compile(r'recipe', re.IGNORECASE)
paren_strip = re.compile(r'\([^)]*(\))?')
# two letters followed by apostrophe "you'll"
poss_strip = re.compile(r"(?<=[a-z][a-z])'(?=[a-z])", re.IGNORECASE)

################
# Extract and modify title and ingredients
################
col_titles = df["title"]
for i in range(0, len(df)):
    
    ################
    # Extract ingredients
    ################
    
    ingreds = df.iloc[i]['ingredients_flat']
    # remove encoded u; prefixes and swap {} -> () for removal
    ingreds = ingreds[1:-1]
    # standard
    ingreds = ingreds.replace("', u'", "', '")
    ingreds = ingreds.replace("': u'", "':'")    
    ingreds = ingreds.replace("{", "(")
    ingreds = ingreds.replace("}", ")")
    ingreds = "{" + ingreds[1:] + "}"
    # strip possessive, cast to lower case
    ingreds = poss_strip.sub("", ingreds).lower()
    ingred_dict = ast.literal_eval(ingreds)
    old_keys = ingred_dict.keys()
    missing_amounts = 0.0
    words_per_ingred = 0.0
    for old_key in old_keys:
        value = ingred_dict.pop(old_key)
        value = value.strip()
        # Count missing amount values:
        if (len(value) < 1):
            missing_amounts = missing_amounts + 1
        # remove parenthesized content from key and value
        new_key = paren_strip.sub("", old_key).strip()
        value = paren_strip.sub("", value).strip()
        # remove periods from keys for mongo
        new_key = new_key.replace(".", "")
        # Sum words for each ingredient
        words_per_ingred = words_per_ingred + (new_key.count(" ") + 1)
        
        ingred_dict[new_key] = value
        
    # Count ingredients
    num_ingreds = len(ingred_dict)
    # Divide total ingredient words by number of ingredients
    words_per_ingred = words_per_ingred  / num_ingreds
    
    df.set_value(i, 'num_ingreds', num_ingreds)
    df.set_value(i, 'ingredients_flat', ingred_dict)
    miss_amt_perc = missing_amounts / num_ingreds
    df.set_value(i, 'miss_amt_perc', miss_amt_perc)
    df.set_value(i, 'words_per_ingred', words_per_ingred)
    
    ################
    # Reduce titles
    ################

    title = df.loc[i, 'title']
    # convert brackets to parens
    title = title.replace("{", "(")
    title = title.replace("}", ")")
    # remove all parens and their contents
    title = paren_strip.sub("", title).strip()
    # remove variants of "slow cooker", "crockpot", "recipe"
    title = sc_strip.sub("", title).strip()
    title = cp_strip.sub("", title).strip()
    title = rcp_strip.sub("", title).strip()
    # update title
    df.set_value(i, 'title', title)

df.to_pickle("df_10k_processed.pkl") 



################
# Insert into mongo
################
'''
title_df = pd.DataFrame(columns=['title'])
for i in range(0, len(df)):
    row = df.iloc[[i]]
    url = row.loc[i, 'url']
    title = row.loc[i, 'title']
    stars = row.loc[i, 'stars']
    reviews = row.loc[i, 'reviews']
    prep_time = float(row.loc[i, 'prep_time'])
    calories_per_serving = row.loc[i, 'calories_per_serving']
    ingred_dict = row.loc[i, 'ingredients_flat']
    flagged = row.loc[i, 'flag']
    # do the insert
    if not flagged:
        document = {
                        'title': title,
                        'url': url,
                        'rating': {
                            'rating': stars,
                            'reviews': reviews
                        },
                        'prep_time': prep_time,
                        'calories_per_serving': calories_per_serving,
                        'ingredients': ingred_dict
                    }
                    
        #db.scr_clean.insert_one(document)
'''
