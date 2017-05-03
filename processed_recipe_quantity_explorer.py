'''
This script was built to explore the different quantities
associated with each unique ingredient in the data set.
The script removes poorly formatted recipes that contain
unspecific names, any missing quantities, or fewer than 4
ingredients. A plot is produced to show the increase in the
variety of units over the number of occurences of an ingredient.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

df = pd.read_pickle("pkls/processed_recipes.pkl")

def getUnit(amount):
    valids = []
    amount = amount.replace(".", "")
    for character in amount:
        if character.isalpha():
            valids.append(character)
    if len(valids) > 0:
        return ''.join(valids)
    else:
        return "missing"

# narrow down the data set
f = 0
p = 0
g = 4
df = df[df.flag <= f]
df = df[df.miss_amt_perc <= p]
df = df[df.num_ingreds >= g]

md = {}
# Building ingredient quantity dictionary: 'garlic' : {'ml': 2, 'clove' : 5 ...}
for i, row in df.iterrows():
    ingreds = row['ingredients_flat']
    for key in ingreds.keys():            
        amt = str(ingreds[key])
        unit = getUnit(amt)
        if key in md.keys():
            if unit in md[key].keys():
                md[key][unit] = md[key][unit] + 1
            else:
                md[key][unit] = 1
        else:
            md[key] = {unit : 1}
     
# transfering dictionary of dictionary to dataframe
cols = ["ingred_name", "units", "variety", "occurrences"]
uni = pd.DataFrame(columns=cols)
for key in md.keys():
    unit_dict = md[key]
    vari = len(md[key])
    occs = sum(unit_dict.values())
    new_row = [key, unit_dict, vari, occs]
    uni.loc[-1] = new_row
    uni.index = uni.index + 1

sns.lmplot(x="occurrences", y="variety", data=uni)

uniques = md.keys()
uniques.sort()
print "Remaining instances: " + str(len(df))
print "Unique Ingredients: " + str(len(uni))
print "Last 20 items: " 
print uniques[-20:]

#uni.to_pickle("pkls/unique_quantified_ingredients.pkl")