###
#
# Script for performing market basket analysis on the prepared data set
#
###

# Load the association rules libraries
library(arules)
library(arulesViz)

mb <- read.transactions("market_basket.csv", format="basket", sep=",")

itemFrequencyPlot(mb, support = 0.08,
                  main="Ingredient: Item Frequency Plot (support=0.08)",
                  xlab="Ingredient", ylab="Frequency"
)

minSup = .005
minConf = .8

##################################
## Create the association model ##
##################################

# Create an association model using the apriori algorithm
# requiring minimum support of 0.01 and minimum confidence of 0.8
rules=apriori(mb, parameter=list(minlen=2, support=minSup, confidence=minConf))

#######################
## Inspect the model ##
#######################

# Scatter plot the rules (confidence, support)
plot(rules);

# Scatter plot the rules (support, lift) with confidence shading
plot(rules, measure=c("support","lift"), shading="confidence");

# Scatter plot the rules (confidence, support) shading by order
plot(rules, shading="order", control=list(main ="Two-key plot"));


# Create a sorted set of rules (confidence descending)
rules.ConfSort = sort(rules, by="confidence", decreasing=TRUE)

# Plot top 50 (confidence) rules as a graph without indicating lift
plot(rules.ConfSort[1:50],method="graph",interactive=FALSE,shading=NA)

# Plot top 50 (confidence) rules as a graph with lift indicator
plot(rules.ConfSort[1:50],method="graph",interactive=FALSE)

# 2D matrix plot of the rules
plot(rules,method="matrix",interactive=FALSE,shading=NA)

# 3D matrix plot of the rules
plot(rules,method="matrix3D",interactive=FALSE,shading=NA)


###################################################
# Create an interactive graph of the top 50 rules #
# (by confidence and with lift indicator)         #
# to allow better exploration and visualization   #
# of the associations found                       #
###################################################
plot(rules.ConfSort[1:50],method="graph",interactive=TRUE)

#########################################################
## Output the Top 10 Rules based on different criteria ##
#########################################################

# Show top 10 rules based on computed quality
print("")
print("Top 10 rules based on quality")
print(head(quality(rules), 10))

# Show top 10 rules based on lift
print("")
print("Top 10 rules based on lift")
print(inspect(head(sort(rules, by="lift", decreasing=TRUE),10)))

# Show top 10 rules based on confidence
print("")
print("Top 10 rules based on confidence")
print(inspect(head(sort(rules, by="confidence", decreasing=TRUE), 10)))

# Show top 10 rules based on support
print("")
print("Top 10 rules based on support")
print(inspect(head(sort(rules, by="support", decreasing=TRUE), 10)))

print("")
print("*** Script reached the end ***")
