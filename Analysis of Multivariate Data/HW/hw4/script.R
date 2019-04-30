library(cluster)
setwd("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/HW/hw4/")
#============================ Reading the data===========
data <- read.csv("oliveoil.csv")
data.area <- data[,1]
data.region <- data[,2]
data.cluster <- data[,-c(1,2)]

#compute the dissimilarity between the objects and normalize them, 
#gower show that we want to apply normalization before computing the dissimilarity 
#matrix


data.dist <- daisy(data.cluster, metric = c("gower"))
#============================= Hierarchical Clustering================
# complete
hc.complete <- agnes(data.dist, method = "complete")
#single
hc.single <- agnes(data.dist, method = "single")
#average
hc.average <- agnes(data.dist, method = "average")

#plotting the hierarchical clustering


png("tree_complete.png", width=3000, height=1500, res=100)
par(cex=0.7)
plot(hc.complete,sub = NA)
dev.off()
png("tree_single.png", width=3000, height=1500, res=100)
par(cex=0.7)
plot(hc.single,sub = NA)
dev.off()
png("tree_average.png", width=3000, height=1500, res=100)
par(cex=0.7)
plot(hc.average,sub = NA)
dev.off()

#cutting trees from hierarchical clustering into 3 different groups
complete.lab <- cutree(hc.complete, 6)
average.lab <- cutree(hc.average,3)
single.lab <- cutree(hc.single,2)


result.complete <- vector()
for (num_of_cluster in 2:10) {
  complete.label <- cutree(hc.complete, num_of_cluster)
  sil_score <- mean(silhouette(complete.label, data.dist)[,3])
  result.complete <- rbind(result.complete, c(num_of_cluster,sil_score))
}
png("silhouette_complete.png", width=2000, height=1500, res=100)
par(cex=2)
plot(silhouette(complete.lab, data.dist), col = "green")
dev.off()
result.average <- vector()
for (num_of_cluster in 2:10) {
  average.label <- cutree(hc.average, num_of_cluster)
  sil_score <- mean(silhouette(average.label, data.dist)[,3])
  result.average <- rbind(result.average, c(num_of_cluster,sil_score))
}
png("silhouette_average.png", width=2000, height=1500, res=100)
par(cex=2)
plot(silhouette(average.lab, data.dist), col = "blue")
dev.off()

result.single <- vector()
for (num_of_cluster in 2:10) {
  single.label <- cutree(hc.single, num_of_cluster)
  sil_score <- mean(silhouette(single.label, data.dist)[,3])
  result.single <- rbind(result.single, c(num_of_cluster,sil_score))
}
png("silhouette_single.png", width=2000, height=1500, res=100)
par(cex=2)
plot(silhouette(single.lab, data.dist), col = "red")
dev.off()

#=========================K-means ====================
library(cluster)
options(warn = 2) 
data.kmeans <- kmeans(data.cluster, centers = 5, nstart = 25)
kmean.label <- data.kmeans$cluster
mean(silhouette(kmean.label, dist(data.cluster))[,3])
resultPam <- vector()
for (num_of_cluster in 2:10 ){
  pam <- pam(data.dist, num_of_cluster, diss=F)
  pam.label <- pam$clustering
  sil_score <- mean(silhouette(pam.label, data.dist)[,3])
  resultPam<- rbind(resultPam, c(num_of_cluster,sil_score))
}
#Partitioning (clustering) of the data into k clusters “around medoids”, a more robust version of K-means
pam <- pam(data.dist, 5, diss=F)
pam.label <- pam$clustering


png("silhouette_pam.png", width=2000, height=1500, res=100)
par(cex=2)
plot(silhouette(pam.label, data.dist), col = "orange")
dev.off()

png("silhouette_kmeans.png",width=2000, height=1500, res=100)
par(cex=2)
plot(silhouette(kmean.label, data.dist), col = "purple")
dev.off()

pambind <- cbind(pam.label, data.cluster)
pambind$pam.label <- as.factor(pambind$pam.label)
str(pambind)
### silhouette for K-means
result <- vector() 
for (num_of_cluster in 2:10 ){
  k.label <- kmeans(data.cluster,num_of_cluster, nstart = 25)$cluster  
  sil_score <- mean(silhouette(k.label, data.dist)[,3])
  result<- rbind(result, c(num_of_cluster,sil_score))
}

#================================== make the tables for each method=====
TCom_area <- table(data.area, complete.lab)
TCom_region <- table(data.region, complete.lab)

TAve_area <- table(data.area, average.lab)
TAve_region <- table(data.region, average.lab)

TSin_area <- table(data.area, single.lab)
TSin_region <- table(data.region, single.lab)

TPam_region <- table(data.region, pam.label)
TPam_area <- table(data.area, pam.label)


Tmeans_region <- table(data.region, kmean.label)
Tmeans_area <- table(data.area, kmean.label)

#=================================== write into text files================
write.table(as.matrix(TCom_region),"hccomplete_region.txt",sep = "\t")
write.table(as.matrix(TCom_area),"hccomplete_area.txt",sep = "\t")
write.table(as.matrix(TAve_region),"hcaverage_region.txt",sep = "\t")
write.table(as.matrix(TAve_area),"hcaverage_area.txt",sep = "\t")
write.table(as.matrix(TSin_region),"hcsingle_region.txt",sep = "\t")
write.table(as.matrix(TSin_area),"hcsingle_area.txt",sep = "\t")
write.table(as.matrix(TPam_region),"pam_region.txt",sep = "\t")
write.table(as.matrix(TPam_area),"pam_area.txt",sep = "\t")
write.table(as.matrix(Tmeans_region),"kmeans_region.txt",sep = "\t")
write.table(as.matrix(Tmeans_area),"kmeans_area.txt",sep = "\t")

