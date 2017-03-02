import pandas as pd
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

df = pd.read_pickle("df_10k_processed.pkl")

# Heuristic 1: Missing amount percentage
# Heuristic 2: Average words per ingredient

# Generate Plot for each heuristic
p_thresh = []
w_thresh = []

h1_rem = []
h2_rem = []

for i in np.arange(0, 10, .1):
    # percent missing will be i / 10 (i=3.5 -> 35%)
    p = i / 10
    # words per ingredient will be i+1
    w = i
    # missing 'amounts' thresholding
    h1_df = df[df.miss_amt_perc <= p]
    h1_rem.append(len(h1_df))
    p_thresh.append(p)
    # Words per Ingred thresholding
    h2_df = df[df.words_per_ingred <= w]
    h2_rem.append(len(h2_df))
    w_thresh.append(w)


fig = plt.figure(1)
fig.clf()
ax1 = fig.add_subplot(121)
ax1.set_title('Percentage Ingreds Missing "amount"')
ax1.set_ylabel("Remaining Recipes")
ax1.set_xlabel("Threshold")
ax2 = fig.add_subplot(122)
ax2.set_title('Average Words per Ingredient Name')
ax2.set_xlabel("Threshold")

ax1.set_ylim(0, 10000)
ax2.set_ylim(0, 10000)
ax1.set_xlim(-.1, 1.1)
ax2.set_xlim(-1, 11)

ax1.scatter(p_thresh, h1_rem, s=45, c='b', label="heuristic 1")
ax2.scatter(w_thresh, h2_rem, s=45, c='r', label="heuristic 2")


# Plot the correlation between the two features

p_corr = df['miss_amt_perc'].values
w_corr = df['words_per_ingred'].values
fig2 = plt.figure(2)
fig2.clf()
ax2_1 = fig2.add_subplot(111)
ax2_1.set_title("Average Words and Missing Amounts")
ax2_1.set_xlabel("Percent Amount Missing")
ax2_1.set_ylabel('Average Words per Ingredient')
ax2_1.scatter(p_corr, w_corr, s=30, c='b')
