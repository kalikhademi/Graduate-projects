library(readxl)
library(normalr)
library(cluster)
require(graphics)
library(Rtsne)
# setwd("~/HXRL/Github/uspermvisaproject/")
setwd("/Users/kianamac/Documents/GitHub/uspermvisaproject/")
#=========================== Reading files ===============================#  

data <- read.csv("Final_data.csv", sep = ',' , header = TRUE)

anyNA(data)


data$employer_yr_estab[data$employer_yr_estab == 14] <- 1986
data$employer_yr_estab[data$employer_yr_estab == 20] <- 1995

data$decision_date <- as.factor(data$decision_date)
data$employer_yr_estab <- as.factor(data$employer_yr_estab)
data$wage_offer_from_9089 <- as.integer(data$wage_offer_from_9089)
data$Employer.State <- as.character(data$Employer.State)
data$Job.State <- as.character(data$Job.State)
data <- data[!is.na(data$employer_yr_estab), ]
data$employer_size[data$employer_size==""]<-"Unknown"
data$Job.State[data$Job.State==""]<-"Unknown"
data$Employer.State[data$Employer.State==""]<-"Unknown"
data$Employer.State <- as.factor(data$Employer.State)
data$Job.State <- as.factor(data$Job.State)

data <- data[,!(names(data) %in% c("X","job_info_alt_occ_job_title","job_info_job_title","wage_offer_unit_of_pay_9089","us_economic_sector","country_of_citizenship"))]

#=========================== Subsampling ===============================#  

smp_siz <- floor(0.1*nrow(data))  # creates a value for dividing the data into train and test. In this case the value is defined as 70% of the number of rows in the dataset
smp_siz  # shows the value of the sample size

train_ind <- sample(seq_len(nrow(data)),size = smp_siz, replace = FALSE)  # Randomly identifies the rows equal to sample size ( defined in previous instruction) from  all the rows of Smarket dataset and stores the row number in train_ind

data.sub <- data[train_ind,] #creates the training dataset with row numbers stored in train_ind
data.test <- data[-train_ind,]

write.csv(data.sub, "subsample_train.csv")
write.csv(data.test, "subsample_test.csv")

visa.diss <- daisy(data.sub[,!(names(data.sub) %in% c("us_economic_sector"))], metric = "gower", type = list(ordratio = c(1,3,6)))
#MDS results 
fit <- cmdscale(visa.diss,eig=TRUE, k=2) 

tsne_label <- data$case_status
data$case_status <- as.factor(data$case_status)

#=========================== Hierarchical Methods ===============================#  

#Single-Linkage
uspermvisa_sgl = agnes(visa.diss,diss = T, metric = "euclidean", stand = F, method = "single")
grp <- cutree(uspermvisa_sgl,k=3)
table(grp)

grp <- cutree(uspermvisa_sgl,k=4)
table(grp)

grp <- cutree(uspermvisa_sgl,k=5)
table(grp)

grp <- cutree(uspermvisa_sgl,k=6)
table(grp)

grp <- cutree(uspermvisa_sgl,k=7)
table(grp)

grp <- cutree(uspermvisa_sgl,k=8)
table(grp)

grp <- cutree(uspermvisa_sgl,k=9)
table(grp)

grp <- cutree(uspermvisa_sgl,k=10)
table(grp)

grp <- cutree(uspermvisa_sgl,k=11)
table(grp)

grp <- cutree(uspermvisa_sgl,k=12)
table(grp)

#Complete Linkage
uspermvisa_com = agnes(data.sub,diss = FALSE, metric = "euclidean", stand = F, method = "complete")
grp <- cutree(uspermvisa_com,k=3)
table(grp)

grp <- cutree(uspermvisa_com,k=4)
table(grp)

grp <- cutree(uspermvisa_com,k=5)
table(grp)

grp <- cutree(uspermvisa_com,k=6)
table(grp)

grp <- cutree(uspermvisa_com,k=7)
table(grp)

grp <- cutree(uspermvisa_com,k=8)
table(grp)

grp <- cutree(uspermvisa_com,k=9)
table(grp)

grp <- cutree(uspermvisa_com,k=10)
table(grp)

grp <- cutree(uspermvisa_com,k=11)
table(grp)

grp <- cutree(uspermvisa_com,k=12)
table(grp)

#Average
uspermvisa_avg = agnes(data,diss = F, metric = "euclidean", stand = F, method = "average")
grp <- cutree(uspermvisa_avg,k=3)
table(grp)

grp <- cutree(uspermvisa_avg,k=4)
table(grp)

grp <- cutree(uspermvisa_avg,k=5)
table(grp)

grp <- cutree(uspermvisa_avg,k=6)
table(grp)

grp <- cutree(uspermvisa_avg,k=7)
table(grp)

grp <- cutree(uspermvisa_avg,k=8)
table(grp)

grp <- cutree(uspermvisa_avg,k=9)
table(grp)

grp <- cutree(uspermvisa_avg,k=10)
table(grp)

grp <- cutree(uspermvisa_avg,k=11)
table(grp)

grp <- cutree(uspermvisa_avg,k=12)
table(grp)

x11()
plot(uspermvisa_sgl)
plot(uspermvisa_com)
plot(uspermvisa_avg)

#Divisive Method

uspermvisa_div = diana(visa.diss, diss = T, metric = "euclidean", stand = F)

plot(uspermvisa_div)

#=========================== Partitioning Methods ===============================#  

#K-Means
cl3 <- kmeans(data,3)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl3$cluster,pch=cl3$cluster,main="K-Means: 3 Clusters")

cl4 <- kmeans(data,4)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl4$cluster,pch=cl4$cluster,main="K-Means: 4 Clusters")

cl5 <- kmeans(data,5)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl5$cluster,pch=cl5$cluster,main="K-Means: 5 Clusters")

cl6 <- kmeans(data,6)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl6$cluster,pch=cl6$cluster,main="K-Means: 6 Clusters")

cl7 <- kmeans(data,7)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl7$cluster,pch=cl7$cluster,main="K-Means: 7 Clusters")

cl8 <- kmeans(data,8)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl8$cluster,pch=cl8$cluster,main="K-Means: 8 Clusters")

cl9 <- kmeans(data,9)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl9$cluster,pch=cl9$cluster,main="K-Means: 9 Clusters")

cl10 <- kmeans(data,10)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl10$cluster,pch=cl10$cluster,main="K-Means: 10 Clusters")

cl11 <- kmeans(data,11)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl11$cluster,pch=cl11$cluster,main="K-Means: 11 Clusters")

cl12 <- kmeans(data,12)
pca.uspermvisa <- princomp(scale(data))
plot(pca.uspermvisa$scores[,1:2],col=cl12$cluster,pch=cl12$cluster,main="K-Means: 12 Clusters")

#PAM 
pam.uspermvisa.3 <- pam(visa.diss, diss= T, k = 3)
clusplot(pam.uspermvisa.3)
plot(pam.uspermvisa.3)

pam.uspermvisa.4 <- pam(data.sub,k = 4)
clusplot(pam.uspermvisa.4)
plot(pam.uspermvisa.4)

pam.uspermvisa.5 <- pam(data.sub, diss = FALSE, k = 5)
clusplot(pam.uspermvisa.5)
plot(pam.uspermvisa.5)

pam.uspermvisa.6 <- pam(data.sub,k = 6)
clusplot(pam.uspermvisa.6)
plot(pam.uspermvisa.6)

pam.uspermvisa.7 <- pam(data.sub,k = 7)
clusplot(pam.uspermvisa.7)
plot(pam.uspermvisa.7)

pam.uspermvisa.8 <- pam(data.sub,k = 8)
clusplot(pam.uspermvisa.8)
plot(pam.uspermvisa.8)

pam.uspermvisa.9 <- pam(data.sub,k = 9)
clusplot(pam.uspermvisa.9)
plot(pam.uspermvisa.9)

pam.uspermvisa.10 <- pam(data.sub,k = 10)
clusplot(pam.uspermvisa.10)
plot(pam.uspermvisa.10)

pam.uspermvisa.11 <- pam(data.sub,k = 11)
clusplot(pam.uspermvisa.11)
plot(pam.uspermvisa.11)

pam.uspermvisa.12 <- pam(data.sub,k = 12)
clusplot(pam.uspermvisa.12)
plot(pam.uspermvisa.12)


