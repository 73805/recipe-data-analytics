import pandas as pd
import operator

'''
This script takes the reduced set of recipes after the 
unique_flattened_ingredients script, and converts each
recipe to a single 1-hot encoded row in a 'market basket' 
table. The columns of this table are the unique ingredients. 
(3000x400)
'''

df = pd.read_pickle("pkls/final_recipe_set.pkl")
df = df.reset_index(drop=True)

# Get the sorted unique ingredient names
uni = pd.read_pickle("pkls/unique_flattened_ingredients.pkl")
uni = uni[uni['occs'] > 1]
uni = uni.sort_values(by='name')
cols = uni['name'].tolist()


# initiate the market basket dataframe
# each row represents a one-hot encoded recipe
# each column is a unique ingredient across the recipes
mb = pd.DataFrame(columns=cols)

# iterate each recipe's ingredints
for i, row in df.iterrows():
    # access ingredient names (no quantities)
    ingreds = row['ingredients_flat']
    ingreds = ingreds.keys()
    # initiate the new row
    mb_row = [0] * len(cols)
    for ing in ingreds:
        # create the 1-hot encoded row
        ind = cols.index(ing)
        mb_row[ind] = 1

    mb.loc[-1] = mb_row
    mb.index = mb.index + 1

mb = mb.drop_duplicates()
mb = mb.reset_index(drop=True)
mb.to_pickle("pkls/market_basket.pkl")
mb.to_csv('one_hot.csv', header=True,index=False)
