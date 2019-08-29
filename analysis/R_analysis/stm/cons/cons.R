# install.packages("igraph")
# install.packages("stmCorrViz")
# install.packages("LDAvis")
library(stm)        # Package for sturctural topic modeling
library(igraph)     # Package for network analysis and visualisation
library(stmCorrViz) # Package for hierarchical correlation view of STMs
library(dplyr)
library(LDAvis)

file_path = "~/Desktop/R/data/company_data/2/1_50_1000_cons.csv"
data <- read.csv(file_path) 
head(data)
dim(data)

processed <- textProcessor(data$Px_Texts, metadata = data, lowercase = FALSE,
                           removestopwords = FALSE, removenumbers = FALSE, removepunctuation = FALSE,
                           stem = FALSE, wordLengths = c(3, Inf), sparselevel = 1,
                           language = "en", verbose = TRUE, onlycharacter = FALSE,
                           striphtml = TRUE, customstopwords = NULL, v1 = FALSE)
# processed <- textProcessor(data$Review_Text, metadata = data, lowercase = TRUE,
#                            removestopwords = TRUE, removenumbers = TRUE, removepunctuation = TRUE,
#                            stem = TRUE, wordLengths = c(3, Inf), sparselevel = 1,
#                            language = "en", verbose = TRUE, onlycharacter = FALSE,
#                            striphtml = TRUE, customstopwords = NULL, v1 = FALSE)
length(processed$vocab)
length(processed$meta)
processed$meta
processed$vocab
processed$documents
length(processed$documents)
dim(processed$meta)
processed$meta['Review_Text']
# out <- prepDocuments(processed$documents, processed$vocab, processed$meta)

out <- prepDocuments(processed$documents, processed$vocab, processed$meta)

docs <- out$documents
vocab <- out$vocab
meta <- out$meta

vignette('stmVignette')
seq(1, 300, by=100)
plotRemoved(processed$documents, lower.thresh=seq(1,300, by=100))


# poliblogPrevFit <- stm(out$documents, out$vocab, K=16, prevalence=~Ratings+Job_Status, 
#                        max.em.its=500, emtol=0, data=out$meta, init.type="Spectral", 
#                        seed=8458159)

poliblogPrevFit <- stm(out$documents, out$vocab, K=10, prevalence=~Ratings+Job_Status+(Reviewed_Year), 
                       data=out$meta, init.type="Spectral", 
                       seed=8458159)


labelTopics(poliblogPrevFit)
summary(poliblogPrevFit)
plot(poliblogPrevFit)
plot(poliblogPrevFit, type="labels", topics=c(1, 2, 4))
sageLabels((poliblogPrevFit))

toLDAvis(poliblogPrevFit, out$documents, R=30 )
corr <- topicCorr(poliblogPrevFit, method="simple", cutoff=.1)
plot(corr, vlabels = c(1:10))

topicQuality(poliblogPrevFit, docs, xlab="Semantic Coherence", 
             ylab="Exclusivity", labels=1:ncol(poliblogPrevFit$theta))

# semanticCoherence(poliblogPrevFit, docs)
# topicQuality(poliblogPrevFit, docs, xlab="Semantic Coherence", 
#              ylab="Exclusivity", labels=c(1:10))

thought <- findThoughts(poliblogPrevFit, texts=as.character(meta$Review_Text), topics=c(1), n=5)
plotQuote(thought$docs[[1]])

findingk <- searchK(out$documents, out$vocab, K=c(8, 10, 16, 20, 30),
                    init.type="Spectral", prevalence =~ Job_Status + Ratings,
                    data=meta, verbose=TRUE)
plot(findingk)

predict_topics <- estimateEffect(formula = 1:10 ~ Ratings + Job_Status + (Reviewed_Year), 
                                 stmobj = poliblogPrevFit, metadata = meta, 
                                 uncertainty = "Global")


cl <- within(as.data.frame(((labelTopics(poliblogPrevFit))$prob)[, 1:3]),   
             V4 <- paste(V1, V2, V3, sep=" "))
typeof(cl$V4)

predict_topics$topics
summary(predict_topics)
# Former Employee --> 0, Current Employee --> 1
plot(predict_topics, covariate = "Job_Status", topics = predict_topics$topics,
     model = poliblogPrevFit, method="difference", labeltype="custom",
     custom.labels = cl$V4, xlab="Former ............ Current",
     main="Effect of Former vs Current(Negative Feedback)",
     cov.value1 = 1, cov.value2 = 0)
plot(predict_topics, covariate = "Ratings", topics = predict_topics$topics,
     model = poliblogPrevFit, method="difference", labeltype="custom",
     custom.labels = cl$V4, xlab="Lower Rating ............ Higher Rating",
     main="Effect of Ratings(Negative Feedback)",
     cov.value1 = 5, cov.value2 = 1)

plot(predict_topics, covariate = "Reviewed_Year", topics = predict_topics$topics,
     model = poliblogPrevFit, method="continuous",
     xlab="Reviewed Year",
     main="Dominant topic over the years",
)


plot(poliblogContent, type="perspectives", topics=7)

sageLabels(poliblogPrevFit)
plot(poliblogPrevFit, type="summary", xlim=c(0,.4))
plot(poliblogPrevFit, type="labels", topics=c(3,7,20))
plot(poliblogPrevFit, type="hist")
plot(poliblogPrevFit, type="perspectives", topics=c(7,10))

poliblogSelect <- selectModel(out$documents, out$vocab, K=20, prevalence=~rating+s(day),
                              max.em.its=75, data=meta, runs=20, seed=8458159)

dim(data)
data[1, ]
