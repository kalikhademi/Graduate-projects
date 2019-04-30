library(caret)
library(rpart.plot)
library(rpart)
library(randomForest)
library(rattle)
setwd("/Users/kianamac/Documents/GitHub/uspermvisaproject/")
# setwd("~/HXRL/Github/uspermvisaproject/")
#=========================== Reading files ===============================#  
 
  data <- read.csv("Final_data.csv", sep = ',' , header = TRUE)
  
  anyNA(data$case_status)
  data$employer_yr_estab[data$employer_yr_estab == 14] <- 1986
  data$employer_yr_estab[data$employer_yr_estab == 20] <- 1995
  
  #data$decision_date <- as.ordered(data$decision_date)
  #data$employer_yr_estab <- as.ordered(data$employer_yr_estab)
  data$wage_offer_from_9089 <- as.integer(data$wage_offer_from_9089)
  data$Employer.State <- as.character(data$Employer.State)
  data$Job.State <- as.character(data$Job.State)
  data <- data[!is.na(data$employer_yr_estab), ]
  
  data$employer_size[data$employer_size==""]<-"Unknown"
  data$Job.State[data$Job.State==""]<-"Unknown"
  data$Employer.State[data$Employer.State==""]<-"Unknown"
  
  data$Employer.State <- as.factor(data$Employer.State)
  data$Job.State <- as.factor(data$Job.State)
  # train_ind <- sample(seq_len(nrow(data)),size = smp_siz, replace = FALSE)  # Randomly identifies the rows equal to sample size ( defined in previous instruction) from  all the rows of Smarket dataset and stores the row number in train_ind
  set.seed(1234)
  train_ind <- sample(1:nrow(data),0.7*nrow(data))
  training <- data[train_ind,] #creates the training dataset with row numbers stored in train_ind
  testing <- data[-train_ind,]
  # training$case_status <- as.factor(training$case_status)
  
training_new <- subset(training, select=-c(X, us_economic_sector, wage_offer_unit_of_pay_9089,employer_name,country_of_citizenship))
testing_new <- subset(testing, select=-c(X, us_economic_sector, wage_offer_unit_of_pay_9089,employer_name,country_of_citizenship))
#=================================== Define models=======================# 
  metric <- "Accuracy"
  DT_model <- train(case_status~., data = training_new, method="rpart",na.action = na.pass, metric= metric)
  Naive_model <- train(case_status~., data = training_new, method = "naive_bayes",na.action = na.pass,metric = metric)
  #RF_model <- train(case_status~., data = training_new, method = "rf",na.action = na.pass, metric = metric)
  RF_model <- randomForest(formula = case_status~., data = training_new, ntree = 1000, importance = T)
  #SVM_model <- train(case_status~., data = training_new, method = "svmLinear",na.action = na.pass, metric = metric)
  #=================================== Visualizations of tree based methods=======================# 
  # rpart.plot(DT_model,box.palette = "RdBu",shadow.col = "gray", nn =TRUE)
  Importance.RF <- varImp(RF_model)
  # plot(Importance.complete, top = 10)
  rpart.plot(DT_model$finalModel)
#============================ Predict using the test data=================#
  DT_predict <- predict(DT_model, newdata = testing_new)
  Naive_predict <-predict(Naive_model, newdata = testing_new)
  RF_predict <- predict(RF_model, newdata = testing_new)
  # svm_predict <- predict(SVM_model,newdata=testing_new)
#========================== construct the confusion matrix===============#
  cm_DT <- confusionMatrix(DT_predict,testing_new$case_status)
  cm_Naive <- confusionMatrix(Naive_predict,testing_new$case_status)
  cm_RF <- confusionMatrix(RF_predict,testing_new$case_status)
  #cm_svm <- confusionMatrix(svm_predict,testing$case_status)
#============================ output files============================================
  # write.table(results_DT,paste(file,"_DT.txt",sep = ""),sep = "\t", row.names = FALSE)
  # write.table(results_NB,paste(file,"_NB.txt",sep = ""),sep = "\t", row.names = FALSE)
  # write.table(results_RF,paste(file,"_RF.txt",sep = ""),sep = "\t", row.names = FALSE)
  # write.table(results_svm,paste(file,"_svm.txt",sep = ""),sep = "\t", row.names = FALSE)
#============================ output confusion matrices================
  write.table(as.matrix(cm_Naive),"Naive_ref.txt",sep = "\t")
  write.table(as.matrix(cm_Naive, what = "overall"),"Naive_overall.txt",sep = "\t")
  write.table(as.matrix(cm_Naive, what = "classes"),"Naive_cls.txt",sep = "\t")
  write.table(as.matrix(cm_DT),"DT_ref.txt",sep = "\t")
  write.table(as.matrix(cm_DT, what = "overall"),"DT_overall.txt",sep = "\t")
  write.table(as.matrix(cm_DT, what = "classes"),"DT_cls.txt",sep = "\t")
  write.table(as.matrix(cm_RF),"RF_ref.txt",sep = "\t")
  write.table(as.matrix(cm_RF, what = "overall"),"RF_overall.txt",sep = "\t")
  write.table(as.matrix(cm_RF, what = "classes"),"RF_cls.txt",sep = "\t")
  