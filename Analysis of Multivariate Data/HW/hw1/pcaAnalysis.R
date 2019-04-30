setwd("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw1/")
data <- read.csv("data.csv",sep=",",header=TRUE,skip=1)
ncolumn <- ncol(data)
#normal_stat <- shapiro.test(data)
data_pca <- data[,-c(108,109)]
library("normalr")
library("ggpubr")
ggdensity(data_pca$V.1, 
          main = "V1",
          xlab = "Tooth length")
ggdensity(data_pca$V.2, 
          main = "V2",
          xlab = "Area")
normalized_data <- normalise(data_pca, lambda = 0)
lshape <- lapply(normalized_data, shapiro.test)
lres <- sapply(lshape, `[`, c("statistic","p.value"))
myfile <- file.path("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw1/", paste0("Normality_result_.csv"))
write.csv(lres, file=myfile,row.names = TRUE,col.names = FALSE)
ggdensity(normalized_data$V.1, 
          main = "norm v1",
          xlab = "Tooth length")
ggdensity(normalized_data$V.2, 
          main = "norm v2",
          xlab = "Area")
library("ggpubr")
pca_cov <- princomp(normalized_data,cor = TRUE)
summary(pca_cov)$loadings[,1:107]
biplot(pca_cov, main="Biplot of two first PCAs")
screeplot(pca_cov,type = "bar",main = "scree plot of PCA components")
summary(pca_cov)
# plot(data[,108],predict(lm_model2))
# abline(lm_model2)
#pca_transformed_data <- as.matrix(data_pca) %*% pca_cov$loadings[,1:30]
barplot(pca_cov$sdev[1:7], main = "PCA eigenvalues")
lm_model <- lm(data[,108]~pca_cov$scores[,1:7])
lm_model1 <- lm(data[,109]~pca_cov$scores[,1:7])
plot(data[,108], predict(lm_model), xlab = "Actual output1", ylab = "Predicted output 1", main = "Predicted vs. Actual", abline(a = 0, b = 1, col = "red"))
plot(data[,109], predict(lm_model1), xlab = "Actual output2", ylab = "Predicted output 2", main = "Predicted vs. Actual", abline(a = 0, b = 1, col = "blue"))
write.csv(pca_cov$loadings[,1:7], file="loadings.csv",row.names = TRUE,col.names = FALSE)
#plot(data[,108],pca_transformed_data)
#abline(lm_model)
#loads_pca_cor <- loadings(pca_cov)
#require(pls)
#pcr_model <- pcr(data[,108]~., data = pca_transformed_data, scale = TRUE, validation = "CV")

