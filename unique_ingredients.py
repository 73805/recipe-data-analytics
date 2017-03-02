import pandas as pd
import unicodedata


df = pd.read_pickle("df_10k_processed.pkl")


p = 0
w = 2.5
df = df[df.miss_amt_perc <= p]
df = df[df.words_per_ingred <= w]

print "Remaining instances: " + str(len(df))


uniques = []
for i in range(0, len(df)):
    ingreds = df.iloc[i]['ingredients_flat']
    for key in ingreds.keys():
        if key not in uniques:
            # key = unicode(key, errors='replace')
            if type(key) == unicode:
                unicodedata.normalize('NFKD', key).encode('ascii', 'ignore').strip()
            else:
                key = unicode(key, 'ascii', 'ignore')
                unicodedata.normalize('NFKD', key).encode('ascii', 'ignore').strip()
            uniques.append(key)
uniques.sort()
print "Number of unique ingredients: " + str(len(uniques))
print "Last 20 items: "
print uniques[-20:]