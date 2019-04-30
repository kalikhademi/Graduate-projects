library(readxl)
library(normalr)
library(cluster)
require(graphics)
library(Rtsne)
# setwd("~/HXRL/Github/uspermvisaproject/")
setwd("C:/Users/Mahdi Kouretchian/Documents/GitHub/uspermvisaproject")
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
data<-sample(1:nrow(data),5000)