library(plyr)
library(dplyr)
library(cluster)
setwd("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/")

#============================ Reading the data===========
df <- read.csv("OnlineNewsPopularity.csv")
df$group<-ifelse(df$shares >1 & df$shares < 946 , 1,

                 ifelse(df$shares >946 & df$shares < 1400, 2,

                        ifelse(df$shares >1400 & df$shares < 2800, 3,

                               ifelse(df$shares > 2800 & df$shares < 843300 ,4 , 0))))

#============================subsampling ====================================================
for ( i in 1:6){
  set.seed(1234)
  sample <- sample(1:nrow(df),2000)
  file7=paste("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/training data/sampletrain",as.character(i),sep = "_")
  write.csv(sample,paste(file7,".csv",sep = ""))
  par(ask=F)
  df[,'group']<-factor(df[,'group'])
  df_train <- df[sample,]
  df_test <- df[-sample,]
  df.group.train <- df_train$group
  df.group.test <- df_test$group
  #df.cluster <- df_train[,-c(1,61,62)]
  file2= paste("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/training data/training",as.character(i),sep = "_")
  write.csv(df_train,paste(file2,".csv",sep = ""))
  file3=paste("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/testing data/testing",as.character(i),sep = "_")
  write.csv(df_test,paste(file3,".csv",sep = ""))
  df_train <- df_train[,-c(1,61,62)]
  df_test <- df_test[,-c(1,61,62)]
  #=======================define complete clustering=========================================
  df.dist <- daisy(df_train)
  hc.complete <- agnes(df.dist, method = "complete")
  complete.lab <- cutree(hc.complete, 4)
  result.complete <- vector()
  for (num_of_cluster in 2:10) {
    complete.label <- cutree(hc.complete, num_of_cluster)
    sil_score <- mean(silhouette(complete.label, df.dist)[,3])
    result.complete <- rbind(result.complete, c(num_of_cluster,sil_score))
  }
  #get the results to know the best number of clusters 
  file = paste("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/complete/results_complete",as.character(i),sep = "_")
  write.csv(result.complete,paste(file,".csv",sep = ""),row.names = TRUE )
  #make the labels 
  file8 = paste("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/complete/complete_label",as.character(i),sep = "_")
  write.csv(complete.lab,paste(file8,".csv",sep = ""),row.names = TRUE )
  #confusion matrix for complete 
  conf_complete <- table(df.group.train, complete.lab)
  file5 = paste("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/complete/conf_complete",as.character(i),sep = "_")
  write.csv(conf_complete, paste(file5,".csv",sep = ""),row.names = TRUE)
  #==========================define pam clustering===============================================
  pam <- pam(df.dist, 2, diss=F)
  pam.label <- pam$clustering
  resultPam <- vector()
  for (num_of_cluster in 2:10 ){
    pam <- pam(df.dist, num_of_cluster, diss=F)
    pam.lab <- pam$clustering
    sil_score <- mean(silhouette(pam.lab, df.dist)[,3])
    resultPam<- rbind(resultPam, c(num_of_cluster,sil_score))
  }
  X11()
  clusplot(pam)
  #get the results to know the best number of clusters
  file1 = paste("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/pam/results_pam",as.character(i),sep = "_")
  write.csv(resultPam,paste(file1,".csv",sep = ""),row.names = TRUE )
  file4 = paste("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/pam/pam_label",as.character(i),sep = "_")
  write.csv(pam.label,paste(file4,".csv",sep = ""),row.names = TRUE )
  conf_pam <- table(df.group.train, pam.label)
  file6 = paste("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw5/pam/conf_pam",as.character(i),sep = "_")
  write.csv(conf_pam,paste(file6,".csv",sep = ""),row.names = TRUE)
  X11()
  plot(silhouette(complete.lab,df.dist), col = "orange")
  X11()
  plot(silhouette(pam.lab,df.dist), col = "blue")
}

