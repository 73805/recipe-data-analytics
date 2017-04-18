###
#
# Script for performing jaccard-based clustering
# on the recipes one-hot encoded table
#
###

# Load the association rules libraries
library(vegan)

mb <- read.csv("one_hot.csv")
d = vegdist(mb, method="jaccard")
hc = hclust(d)
plot(hc)

clusterCut <- cutree(hc,50)