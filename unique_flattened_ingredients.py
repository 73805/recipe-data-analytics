import pandas as pd

df = pd.read_pickle("pkls/processed_pickle.pkl")

# narrow down the data set
f = 0
g = 4
df = df[df.flag <= f]
df = df[df.num_ingreds >= g]

uniques = {}
# Building flattened list of ingredient names
for i, row in df.iterrows():
    ingreds = row['ingredients_flat']
    for ing in ingreds.keys():
        if ing not in uniques:
            uniques[ing] = 1
        else:
            uniques[ing] = uniques[ing] + 1

unikeys = uniques.keys()
unikeys.sort()
print "Remaining instances: " + str(len(df))
print "Unique Ingredients: " + str(len(unikeys))
print "Last 20 items: "
print unikeys[-20:]

cols = ["name", "occs"]
uni = pd.DataFrame(columns=cols)
for key in uniques.keys():
    occs = uniques[key]
    new_row = [key, occs]
    uni.loc[-1] = new_row
    uni.index = uni.index + 1

uni.to_pickle("pkls/unique_flattened_ingredients.pkl") 