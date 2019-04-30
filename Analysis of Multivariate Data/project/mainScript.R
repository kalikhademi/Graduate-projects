#setwd("~/Courses/STA6707/Project/")
setwd("/Users/kianamac/Documents/GitHub/uspermvisaproject/")
#read the two other scripts
source("classification.R")
source("clustering.R")


data <- read.csv("Final_data.csv", sep = ',' , header = TRUE)
classification(data)

clustering(data)

