import pandas as pd
import unicodedata
import re
import ast

df = pd.read_pickle("pkls/full_10k.pkl")

paren_strip = re.compile(r'\([^)]*(\))?')
# two letters followed by apostrophe "you'll"
poss_strip = re.compile(r"(?<=[a-z][a-z])'(?=[a-z])", re.IGNORECASE)

# Function to convert ingredient strings to ascii
def asciify(st):
    if type(st) == unicode:
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    else:
        st = unicode(st, 'ascii', 'ignore')
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    return st


################
# Iterate rows to generate additional Ingredient Features
################

for i, row in df.iterrows():

    ingreds = row['ingredients_flat']

    old_keys = ingreds.keys()
    missing_amounts = 0.0
    words_per_ingred = 0.0
    for old_key in old_keys:
        value = ingreds.pop(old_key)
        value = value.strip()
        # Count missing amount values:
        if (len(value) < 1):
            missing_amounts = missing_amounts + 1
        # remove parenthesized content from key and value
        value = value.replace("{", "(").replace("}", ")")
        new_key = old_key.replace("{", "(").replace("}", ")")
        new_key = paren_strip.sub("", old_key).strip()
        value = paren_strip.sub("", value).strip()
        # remove periods from keys for mongo
        new_key = new_key.replace(".", "")
        
        # Getting the encoding right
        new_key = asciify(new_key).lower()
        value = asciify(value).lower()
        
        # Sum words for each ingredient
        words_per_ingred = words_per_ingred + (new_key.count(" ") + 1)

        ingreds[new_key] = value

    # Count ingredients
    num_ingreds = len(ingreds)
    # Divide total ingredient words by number of ingredients
    if num_ingreds > 0:
        words_per_ingred = words_per_ingred / num_ingreds
        miss_amt_perc = missing_amounts / num_ingreds
    else:
        words_per_ingred = float('NaN')
        miss_amt_perc = float('NaN')

    df.set_value(i, 'num_ingreds', num_ingreds)
    df.set_value(i, 'miss_amt_perc', miss_amt_perc)
    df.set_value(i, 'words_per_ingred', words_per_ingred)
    # convert dict to string for duplicate parsing
    df.set_value(i, 'ingredients_flat', str(ingreds))

# remove duplicates
df = df.drop_duplicates(subset='ingredients_flat', keep='last')
# revert strings to dictionaries
for i, row in df.iterrows():
    ingreds = row['ingredients_flat']
    if len(ingreds) > 0:
        ingreds = ast.literal_eval(ingreds)
    else:
        ingreds = {}
    df.set_value(i, 'ingredients_flat', ingreds)

df.to_pickle("pkls/processed_pickle.pkl") 