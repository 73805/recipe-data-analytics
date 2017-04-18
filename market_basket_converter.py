import pandas as pd

'''
This script takes the one-hot encoded matrix and converts
it into an R association rules style CSV. 
Each row is a recipe, and each cell in a row is any of the ingredients
in that recipe.

'''

df = pd.read_pickle("pkls/final_recipe_set.pkl")
df = df.reset_index(drop=True)

# Get the sorted unique ingredient names
uni = pd.read_pickle("pkls/unique_flattened_ingredients.pkl")
uni = uni[uni['occs'] > 1]
uni = uni.sort_values(by='name')
cols = uni['name'].tolist()

maxlen = 0
# convert ingredient dictionaries to lists of ingredient names
for i, row in df.iterrows():
    # access ingredient names (no quantities)
    ingreds = row['ingredients_flat']
    ingreds = ingreds.keys()
    if len(ingreds) > maxlen:
        maxlen = len(ingreds)
    df.set_value(i,'ingredients_flat', ingreds)

# initiate the market basket dataframe
# to create complete rows, each list of ingredients
# will be extended with 0's to reach the max row len
mb = pd.DataFrame(columns=range(0,maxlen))

for i, row in df.iterrows():
    mb_row = row['ingredients_flat']
    # filter out garlic and onion
    mb_row = filter(lambda z: z != 'garlic', mb_row)
    mb_row = filter(lambda z: z != 'onion', mb_row)
    # extend with 0's (remove in excel)
    dif = maxlen - len(mb_row)
    mb_row = mb_row + ([0] * dif)
    mb.loc[-1] = mb_row
    mb.index = mb.index + 1

mb = mb.drop_duplicates()
mb = mb.reset_index(drop=True)
mb.to_csv('market_basket_no_gar-oni.csv', header=False,index=False)