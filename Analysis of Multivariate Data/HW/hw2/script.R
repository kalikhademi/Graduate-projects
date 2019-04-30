setwd("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw2/")

data <- read.csv("arrhythmia.csv",sep =",",header = FALSE)
headers <- read.csv("headers.csv",sep =",",header = TRUE)
colnames(data )<- colnames(headers)

write.csv(data, file = "data.csv",col.names = FALSE,row.names = FALSE)
