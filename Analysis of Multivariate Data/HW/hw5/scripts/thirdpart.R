
library(plyr)
library(dplyr)
library(randomForest)
library(caret)
library(adabag)
library(rpart)
setwd("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/")

#============================ Reading the data========================


df <- read.csv("OnlineNewsPopularity.csv")
df_train <- read.csv("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/training data/training_1.csv")
df_test <- read.csv("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/testing data/testing_1.csv")
df_train_complete_label <- read.csv("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/complete/complete_label_1.csv")
df_train_pam_label <- read.csv("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/pam/pam_label_1.csv")
df_train_pam_label<- as.factor(df_train_pam_label$x)
df_train_complete_label <- as.factor(df_train_complete_label$x)
df.train.pam <- cbind(df_train,df_train_pam_label)
df.train.complete <- cbind(df_train,df_train_complete_label)
df.train.complete <- df.train.complete[,!names(df.train.complete) %in% c("X", "url","shares","group")]
df.train.pam <- df.train.pam[,!names(df.train.pam) %in% c("X","url","shares","group")]
#==============================define random forest with complete label====================
RF_model_complete <- train(df_train_complete_label~., data = df.train.complete,  method="rf",importance= TRUE )
RF_predict_complete <- predict(RF_model_complete, newdata = df_test)
Importance.complete <- varImp(RF_model_complete)
plot(Importance.complete, top = 10)
#============================define ada boosting algorithm with complete label===================
df.adaboost.complete <- boosting(df_train_complete_label ~ ., data = df.train.complete,boos= TRUE, mfinal =20)
boost_predict_complete<- predict(df.adaboost.complete,newdata=df_test)
t1<-df.adaboost.complete$trees[[1]]
library(tree)
plot(t1)
text(t1,pretty=0)
varplot(df.adaboost.complete)
#==============================define random forest with pam label====================
RF_mode_pam <- train(df_train_pam_label~., data = df.train.pam, method="rf", importance= TRUE )
RF_predict_pam <- predict(RF_mode_pam, newdata = df_test)
Importance.pam <- varImp(RF_mode_pam)
plot(Importance.pam, top = 10)
#============================define ada boosting algorithm with pam label===================
df.adaboost.pam <-boosting(df_train_pam_label ~ ., data = df.train.pam,boos= TRUE, mfinal =20)
boost_predict_pam <- predict(df.adaboost.pam,newdata=df_test)
t1<-df.adaboost.pam$trees[[1]]
plot(t1)
varplot(df.adaboost.pam)

#================================= output the frequency tables==================================

freq_table_rf_complete <- table(RF_predict_complete$class)
freq_table_rf_pam <- table(RF_predict_pam$class)
freq_table_boost_pam <- table(boost_predict_pam$class)
freq_table_boost_complete <- table(boost_predict_complete$class)
write.csv(freq_table_boost_pam,file = "freq_boost_third.csv",row.names = TRUE)
write.csv(freq_table_boost_complete,file = "freq_boost_third.csv",row.names = TRUE)
write.csv(freq_table_rf_pam,file = "freq_rf_third_pam.csv",row.names = TRUE)
write.csv(freq_table_rf_complete,file = "freq_rf_third_complete.csv",row.names = TRUE)