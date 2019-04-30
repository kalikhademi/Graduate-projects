
library(plyr)
library(dplyr)
library(randomForest)
library(caret)
library(adabag)
setwd("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/")

#============================ Reading the data========================
df <- read.csv("OnlineNewsPopularity.csv")
df$group<-ifelse(df$shares >1 & df$shares < 946 , 1,
                 
                 ifelse(df$shares >946 & df$shares < 1400, 2,
                        
                        ifelse(df$shares >1400 & df$shares < 2800, 3,
                               
                               ifelse(df$shares > 2800 & df$shares < 843300 ,4 , 0))))
df[,'group']<-factor(df[,'group'])
df <- df[,-c(1,61)]
trainIndex <- createDataPartition(df$group, p=0.7, list=FALSE)
df_train <- df[trainIndex,]
df_test <- df[-trainIndex,]

#==============================define random forest====================
RF_model <- randomForest(group~., data = df_train,ntree = 500, importance= TRUE )
RF_predict <- predict(RF_model, newdata = df_test)
#cm_RF <- confusionMatrix(RF_predict,df_test$group)
cm_RF <- table(df_test$group, RF_predict)
cm_rf_acc <- sum(diag(cm_RF))/sum(cm_RF)*100
write.csv(cm_RF,file = "confusion_RF_first.csv",row.names = TRUE)
importance(RF_model)
varImpPlot(RF_model)
#============================define ada boosting algorithm===================
df.adaboost <- boosting(group ~ ., data = df_train, boos = TRUE, mfinal = 20)
boost_predict <- predict(df.adaboost,newdata=df_test)
cm_boost <- boost_predict$confusion
cm_boost_acc <- sum(diag(cm_boost))/sum(cm_boost)*100
cm_boost_acc
write.csv(cm_boost,file = "confusion_boost_first.csv",row.names = TRUE)
t1<-df.adaboost$trees[[1]]
plot(t1)
varplot(df.adaboost)
errorevol(df.adaboost,df_train)
freq_table_rf <- table(RF_predict$class)
freq_table_boost <- table(boost_predict$class)
write.csv(freq_table_boost,file = "freq_boost_first.csv",row.names = TRUE)
write.csv(freq_table_rf,file = "freq_rf_first.csv",row.names = TRUE)  