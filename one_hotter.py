'''
This script takes the reduced set of recipes after the 
unique_flattened_ingredients script, and converts each
recipe to a single 1-hot encoded row in a 'market basket' 
table. The columns of this table are the unique ingredients. 
(3000x400)
'''

import pandas as pd
from sklearn.model_selection import train_test_split
import unicodedata
import re


def asciify(st):
    if type(st) == unicode:
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    else:
        st = unicode(st, 'ascii', 'ignore')
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    return st


# Regular expressions to remove common substrings from the titles
sc_strip = re.compile(r'slow[-|\s]?cooke[r|d]\s?', re.IGNORECASE)
cp_strip = re.compile(r'crock[-|\s]?pot\s?', re.IGNORECASE)
rcp_strip = re.compile(r'recipe', re.IGNORECASE)


df = pd.read_pickle("pkls/final_recipe_set.pkl")
df = df.reset_index(drop=True)

# Get the sorted unique ingredient names
uni = pd.read_pickle("pkls/unique_flattened_ingredients.pkl")
uni = uni[uni['occs'] > 1]
uni = uni.sort_values(by='name')
cols = uni['name'].tolist()
cols.insert(0, 'title')
ings = cols[1:]

# initiate the market basket dataframe
# each row represents a one-hot encoded recipe
# each column is a unique ingredient across the recipes
mb = pd.DataFrame(columns=cols)

# iterate each recipe's ingredints
for i, row in df.iterrows():
    # initiate the new row
    mb_row = [0] * len(cols)
    # Clean up the title
    name = row['title']
    name = asciify(name)
    name = cp_strip.sub("", name).strip()
    name = sc_strip.sub("", name).strip()
    name = rcp_strip.sub("", name).strip()
    mb_row[0] = name
    # one-hot encode the ingredients (out of dictionary)
    ingreds = row['ingredients_flat']
    ingreds = ingreds.keys()
    ingreds = filter(lambda z: z != 'garlic', ingreds)
    ingreds = filter(lambda z: z != 'onion', ingreds)
    for ing in ingreds:
        # 1-hot encode each ingredient
        ind = ings.index(ing)
        mb_row[ind + 1] = 1
    mb.loc[-1] = mb_row
    mb.index = mb.index + 1

mb = mb.drop_duplicates()
mb = mb.reset_index(drop=True)

# Save out a subset
subset_size = 1000.0
split_size = subset_size / len(df)
train, test = train_test_split(df, test_size = split_size)
test.to_csv('one_hot_subset.csv', header=True,index=False, ecoding='utf-8')

mb.to_csv('one_hot_named_no_gar.csv', header=True,index=False, ecoding='utf-8')
