setwd("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw2/")

# data <- read.csv("arrhythmia.csv",sep =",",header = FALSE)
# headers <- read.csv("headers.csv",sep =",",header = TRUE)
# colnames(data )<- colnames(headers)
# 
# write.csv(data, file = "data.csv",col.names = FALSE,row.names = FALSE)
data <- read.csv("data.csv",sep =",",header = TRUE)
#------------------------------- check the formats of the data----------------------------------------
data$Sex <- factor(data$Sex)
data$T <- as.integer(data$T)
data$P <- as.integer(data$P)
data$QRST <- as.integer(data$QRST)
#data$class <- factor(data$class)
data$Heart.rates <- as.integer(data$Heart.rates)
#-------------------------------- remove minority classes for QDA-----------------------------------

data <- subset(data, class != "0")
data$class <- droplevels(data$class, exclude = 0)
# data <- subset(data, class != "7")
# data$class <- droplevels(data$class, exclude = 7)
# data <- subset(data, class != "8")
# data$class <- droplevels(data$class, exclude = 8)
# data <- subset(data, class != "14")
# data$class <- droplevels(data$class, exclude = 14)
# data <- subset(data, class != "15")
# data$class <- droplevels(data$class, exclude = 15)


#------------------------------ replacing the question marks-----------------------
for(i in (1:ncol(data))){
  if(sapply(data[,i],is.factor) == TRUE){
    mean_i <- sapply(data[,i], mean)
    data[,i] <- gsub("?",mean_i,data[,i], fixed = TRUE)
    data[,i] <- as.factor(data[,i])
  }
  if(sapply(data[,i],is.integer) == TRUE){
    mean_i <- sapply(data[,i], mean)
    data[,i] <- gsub("?",mean_i,data[,i], fixed = TRUE)
    data[,i] <- as.integer(data[,i])
  }
  
}

write.csv(data, file="output_clean.csv",row.names = FALSE)

