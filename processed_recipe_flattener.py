'''
This script takes the procesed recipes, removes poorly conditioned
recipes, and iterates the remaining recipe ingredient lists
to extract the unique ingredients as a dataframe of ingredient names
and occurence counts.
Poorly conditioned recipes are defined as recipes that have
any ingredients with 'unspecific' names as indicated by the lack
of a specific <a> tag wrapping a small segment of the name. The
absence of this tag was flagged by incrementing the 'flag' feature.
'''

import pandas as pd

df = pd.read_pickle("pkls/processed_recipes.pkl")

# Remove recipes with unspecific ingred names or fewer than 4 ingreds
f = 0
g = 4
df = df[df.flag <= f]
df = df[df.num_ingreds >= g]
print "Remaining instances: " + str(len(df))

# Building a list of unique ingredient names : counts
uniques = {}
for i, row in df.iterrows():
    ingreds = row['ingredients_flat']
    for ing in ingreds.keys():
        if ing not in uniques:
            uniques[ing] = 1
        else:
            uniques[ing] = uniques[ing] + 1

unikeys = uniques.keys()
unikeys.sort()
# Print out some data about the unique ingredient names
print "Numer of Unique Ingredients: " + str(len(unikeys))
print "Last 20 Unique Ingredients: "
print unikeys[-20:]

# Package into a data frame
cols = ["name", "occs"]
uni = pd.DataFrame(columns=cols)
for key in uniques.keys():
    occs = uniques[key]
    new_row = [key, occs]
    uni.loc[-1] = new_row
    uni.index = uni.index + 1

uni.to_pickle("pkls/unique_flattened_ingredients.pkl")

# Remove all recipes that contain a one-time ingredient.
# Many one-time ingredients are not really ingredients.

uni = uni[uni['occs'] == 1]
oneTimer = uni['name'].tolist()

df = df.reset_index(drop=True)
dl = []
# get indices of recipes containing a 1-time ingredient for removal
for i, row in df.iterrows():
    ingreds = row['ingredients_flat']
    for ing in ingreds.keys():
        if ing in oneTimer:
            dl.append(i)

df = df.drop(df.index[dl])
df = df.reset_index(drop=True)

df.to_pickle("pkls/final_recipe_set.pkl")
