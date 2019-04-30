setwd("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw3/area/")
library(MASS)
library(caret)
library(rpart.plot)
require(randomForest)
#------------------------------------- Read Files------------------------------------------------------------------
dataset <- read.csv("oliveoil.csv",sep = ',', header = TRUE)
colnames(dataset)[colnames(dataset)=="macro.area"] <- "area" 
trainIndex <- createDataPartition(dataset$region, p=0.7, list=FALSE)
data_train <- dataset[trainIndex,]
data_test <- dataset[-trainIndex,]

#------------------------------------ Cross Validation---------------------------------------------------------------
train.control <- trainControl(method = "cv",number =10)

LDA_model <- train(area ~ palmitic+palmitoleic+stearic+oleic+linoleic+linolenic+arachidic+eicosenoic , data = data_train, method = "lda",trControl = train.control)
QDA_model <-train(area ~ palmitic+palmitoleic+stearic+oleic+linoleic+linolenic+arachidic+eicosenoic , data = dataset, method = "qda",trControl = train.control) 
DT_model <- train(area ~palmitic+palmitoleic+stearic+oleic+linoleic+linolenic+arachidic+eicosenoic, data = data_train, method = "rpart",trControl = train.control)
RF_model <- randomForest(area ~palmitic+palmitoleic+stearic+oleic+linoleic+linolenic+arachidic+eicosenoic, data = data_train, ntree= 33, method = "rf",trControl = train.control,importance= TRUE )
KNN_model <-train(area ~palmitic+palmitoleic+stearic+oleic+linoleic+linolenic+arachidic+eicosenoic, data = data_train, method = "knn",trControl = train.control,tuneGrid = expand.grid(k = 1:25))
SVM_model <-train(area ~palmitic+palmitoleic+stearic+oleic+linoleic+linolenic+arachidic+eicosenoic, data = data_train, method = "svmLinear",trControl = train.control)
Naive_model <- train(area ~ palmitic+palmitoleic+stearic+oleic+linoleic+linolenic+arachidic+eicosenoic, data = data_train, method = "naive_bayes",trControl = train.control)
prp(DT_model$finalModel, box.palette = "Reds", tweak = 1.2)
importance(RF_model)
varImpPlot(RF_model)
#------------------------------------ Region Prediction model definition--------------------------------------------
LDA_predict <- predict(LDA_model, newdata= data_test)
QDA_predict <- predict(QDA_model,newdata = data_test)
DT_predict <- predict(DT_model, newdata = data_test)
RF_predict <- predict(RF_model, newdata = data_test)
KNN_predict <-predict(KNN_model, newdata = data_test)
SVM_predict <-predict(SVM_model, newdata = data_test)
Naive_predict <-predict(Naive_model, newdata = data_test)
#----------------------------------------- Assess the model performance----------------------------------------------
cm_DT <- confusionMatrix(DT_predict,data_test$area)
cm_RF <- confusionMatrix(RF_predict,data_test$area)
cm_KNN <- confusionMatrix(KNN_predict,data_test$area)
cm_SVM <- confusionMatrix(SVM_predict,data_test$area)
cm_Naive <- confusionMatrix(Naive_predict,data_test$area)
cm_LDA <- confusionMatrix(LDA_predict,data_test$area)
cm_QDA <- confusionMatrix(QDA_predict,data_test$area)
#-------------------------------------------- write into files------------------------------------------------------
write.table(as.matrix(cm_DT),"results_DT.txt",sep = "\t")
write.table(as.matrix(cm_DT, what = "overall"),"results_overall_DT.txt",sep = "\t")
write.table(as.matrix(cm_DT, what = "classes"),"results_cls_DT.txt",sep = "\t")
#-------------------
write.table(as.matrix(cm_RF),"results_RF.txt",sep = "\t")
write.table(as.matrix(cm_RF, what = "overall"),"results_overall_RF.txt",sep = "\t")
write.table(as.matrix(cm_RF, what = "classes"),"results_cls_RF.txt",sep = "\t")
#-----------------
write.table(as.matrix(cm_KNN),"results_knn.txt",sep = "\t")
write.table(as.matrix(cm_KNN, what = "overall"),"results_overall_knn.txt",sep = "\t")
write.table(as.matrix(cm_KNN, what = "classes"),"results_cls_knn.txt",sep = "\t")
#-------------------
write.table(as.matrix(cm_SVM),"results_svm.txt",sep = "\t")
write.table(as.matrix(cm_SVM, what = "overall"),"results_overall_svm.txt",sep = "\t")
write.table(as.matrix(cm_SVM, what = "classes"),"results_cls_svm.txt",sep = "\t")
#-------------------
write.table(as.matrix(cm_Naive),"results_naive.txt",sep = "\t")
write.table(as.matrix(cm_Naive, what = "overall"),"results_overall_naive.txt",sep = "\t")
write.table(as.matrix(cm_Naive, what = "classes"),"results_cls_naive.txt",sep = "\t")
#-------------------
write.table(as.matrix(cm_LDA),"results_lda.txt",sep = "\t")
write.table(as.matrix(cm_LDA, what = "overall"),"results_overall_lda.txt",sep = "\t")
write.table(as.matrix(cm_LDA, what = "classes"),"results_cls_lda.txt",sep = "\t")
#--------------------------------
write.table(as.matrix(cm_QDA),"results_qda.txt",sep = "\t")
write.table(as.matrix(cm_QDA, what = "overall"),"results_overall_qda.txt",sep = "\t")
write.table(as.matrix(cm_QDA, what = "classes"),"results_cls_qda.txt",sep = "\t")