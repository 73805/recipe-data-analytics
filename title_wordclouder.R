library(tm)
library(wordcloud)
library(RColorBrewer)

# Instruction from: http://analyticstraining.com/2014/how-to-create-a-word-cloud-in-r/

mb <- read.csv("one_hot_named_no_gar.csv")
names(mb)[1] <- 'titles'

titles_text <- Corpus(VectorSource(mb$titles))

titles <- Corpus(VectorSource(titles_text))

titles_data <- tm_map(titles,stripWhitespace)
titles_data <- tm_map(titles,tolower)
titles_data <- tm_map(titles,removeNumbers)
titles_data <- tm_map(titles,removePunctuation)
titles_data <- tm_map(titles,removeWords,stopwords("english"))


tdm_titles<-TermDocumentMatrix (titles_data) #Creates a TDM

TDM1<-as.matrix(tdm_titles) #Convert this into a matrix format

v = sort(rowSums(TDM1), decreasing = TRUE) #Gives you the frequencies for every word

wordcloud (titles_data, scale=c(5,.8), max.words=200, random.order=FALSE, rot.per=0, use.r.layout=FALSE, colors=brewer.pal(8, "Spectral"))