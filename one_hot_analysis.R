###
#
# Script for performing jaccard-based clustering
# on the recipes one-hot encoded table
#
###

# Load hierarchical clustering libraries
library(vegan)
library(cluster)
library(tm)
library(wordcloud)

mb <- read.csv("one_hot_named_no_gar-oni.csv")
names(mb)[1] <- 'titles'

dat <- mb[,c(2:length(mb))]
dist = vegdist(dat, method="jaccard")
hc = hclust(dist)

# loop to look at different distributions of clusters.

for (i in seq(5,150,5)){
  clusts <- cutree(hc, i)
  hist(clusts, breaks=c(1:i), ylim=c(0,130))
}

if(FALSE){
# 105 looked best, and 75 looked like a good threshold for support
count = 105
clusts <- cutree(hc, count)
mb$clusts = clusts

thresh = 75

for (i in c(1:count)){
  clust = mb[mb$clusts == i,]
  if(nrow(clust) >= thresh){
    titles <- Corpus(VectorSource(clust$title))
    
    titles_data <- tm_map(titles,tolower)
    titles_data <- tm_map(titles,removeNumbers)
    titles_data <- tm_map(titles,removePunctuation)
    titles_data <- tm_map(titles,removeWords,stopwords("english"))
    
    tdm_titles <- TermDocumentMatrix(titles_data)
    TDM1 <- as.matrix(tdm_titles)
    v = sort(rowSums(TDM1), decreasing = TRUE)
    
    wordcloud (titles_data, scale=c(5,2), max.words=10, random.order=FALSE, rot.per=0, use.r.layout=FALSE, colors=brewer.pal(8, "Spectral"))
  }
}
}
  
  
  
  
  
  
  
  
  