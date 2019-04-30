setwd("c:/Users/Mahdi Kouretchian/Desktop/applied multivariable analysis/reports/homework2")
library(devtools)
library(caret)
require(MASS)
library(rpart.plot)
library(rpart)
library(devtools)
source("dqda.R")
library("normalr")

#read the cleaned data file and remove the ones which are completely zero
clean_data <- read.csv("output_clean.csv",sep =",",header = TRUE)
clean_data <-clean_data[,apply(clean_data,2,function(clean_data) !all(clean_data==0))]
write.csv(clean_data,file="output2.csv",row.names = FALSE)
labels_data <- factor(clean_data$class)

#------------------------------- checking the normality----------------------------
lshape <- lapply(clean_data, shapiro.test)
lres <- sapply(lshape, `[`, c("statistic","p.value"))
#myfile <- file.path("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw2/", paste0("Normality_result_.csv"))
#write.csv(lres, file=myfile,row.names = TRUE,col.names = FALSE)
clean_data <- clean_data[,-c(279)]
#clean_data_pca <- normalise(clean_data, lambda = 0)
#clean_data_pca <- clean_data_pca[,-c(279)]
#-------------------------------Computing PCA---------------------------------------
pca_model <- prcomp(clean_data, scale = TRUE, center = TRUE)
summary(pca_model)
pr.var <- pca_model$sdev ^ 2
pve_cor <- pr.var/sum(pr.var)
variance_cov <- round(pve_cor, 2)
eigenvalues <- round(pr.var,2)
cumulative_var <- round(cumsum(pve_cor), 2)
#plot covariance matrix 
plot(pve_cor, xlab = "Principal Component", 
     ylab = "Proportion of Variance Explained", type = "b")

plot(cumulative_var, xlab = "Principal Component", 
     ylab = "Cumulative Proportion of Variance Explained", 
     ylim = c(0, 1), type = "b")

#-------------------------------Form the data using the PCs--------------------------
pcs_component <- pca_model$x[,1:50]
final_pca_data <- pcs_component
final_pca_data <- as.data.frame(cbind(pcs_component,labels_data))
#----------------------------------Data Splitting---------------------------------
N <- nrow(final_pca_data)
rvec <- runif(N)
final_pca_data$labels_data <- factor(final_pca_data$labels_data)
training <- final_pca_data[rvec < 0.75,]
testing <- final_pca_data[rvec >= 0.75,]
nrow(training)
nrow(testing)
training <- as.data.frame(training)
testing <- as.data.frame(testing)
#----------------------------------------Apply LDA-------------------------------
LDA_model<-lda(labels_data~.,data =training)
predict_model_LDA <- predict(LDA_model,newdata = testing)
out.lda = confusionMatrix(testing$labels_data, predict_model_LDA$class)
#table(predicted= predict_model$class,actual = labels_data)
#----------------------------------------Apply QDA-------------------------------
set.seed(3033)
#clean_data$class <- factor(clean_data$class)
intrain_QDA <- createDataPartition(y = clean_data$class, p= 0.7, list = FALSE)
training_QDA <- clean_data[intrain_QDA,]
testing_QDA <- clean_data[-intrain_QDA,]
QDA_model<-dqda(class~.,data =training_QDA)
predict_model_QDA <- predict(QDA_model,testing_QDA)
#table(predicted= predict_model$class,actual = labels_data)

#----------------------------------------Decision Tree-------------------------------
#Apply Decision Tree
set.seed(3033)
clean_data$class <- factor(clean_data$class)
intrain_DT <- createDataPartition(y = clean_data$class, p= 0.7, list = FALSE)
training_DT <- clean_data[intrain_DT,]
testing_DT <- clean_data[-intrain_DT,]
training_DT = na.omit(training_DT)
testing_DT = na.omit(testing_DT)
trctrl <- trainControl(method = "repeatedcv", number = 10, repeats = 3)
set.seed(3333)
dtree_fit <- train(factor(class) ~., data = training_DT, method = "rpart", 
                   parms = list(split = "gini"),
                   trControl=trctrl,
                   tuneLength = 10)
rpart.plot(dtree_fit$finalModel, box.palette = "Reds", tweak = 1.2)
test_pred <- predict(dtree_fit, newdata = testing_DT,na.action = na.pass)
confusionMatrix(table(test_pred, testing_DT$class))
