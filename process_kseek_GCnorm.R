read.table('merge_kseek_30x.rep.GCnorm.filter.names', header=T) -> kseek
kcounts <- kseek[-1]
tcounts <- t(kcounts)
k.pca <- prcomp(tcounts, center=TRUE, scale.=TRUE)
library(ggbiplot)
library(ggfortify)
library(cluster)
autoplot(k.pca)
mouseline=c('BL6','BL6','BL6','BL6','BL6','BL6','BL10','BL10','BL10','BL6','BL10','BL6','BL6','BL10')
population=rownames(tcounts)
klabs=cbind(mouseline, tcounts)
knames=cbind(population, tcounts)
autoplot(k.pca, data=klabs, colour="mouseline", frame=T, frame.type="norm")
autoplot(k.pca, data=knames, label=TRUE)

stdev=k.pca$sdev
prvar=stdev^2
propvar=prvar/sum(prvar)
plot(propvar, xlab="Principal Component", ylab="Proportion of Variance Explained", type="b")

nmd = kseek
nmd[2:15]=round(nmd[2:15])
clusterdfplot = function(dataframe,numrows,col="sky",main="Bar Graph",size=.75){
  numcol=ncol(dataframe)
  df = dataframe[1:numrows,2:numcol]
  mat = do.call(rbind,df)
  colnames(mat) = unlist(dataframe[1:numrows,1])
  mat = apply(mat,c(1,2),as.numeric)
  color=c("red", "orange", "yellow", "green", "darkgreen", "navy", "mediumblue", "lightblue",
          "mediumorchid", "darkorchid", "purple", "magenta", "deeppink", "pink") 
  #  color = colors()[grep(col,colors())]
  barplot(mat,beside=T,main=main,col=color,legend.text=rownames(mat),args.legend=list(x="topright",bty="n",cex=size),las=2,cex.names=.5)
}
ncol=ncol(nmd)
nrows=nrow(nmd)
nmd$Sum=0
for (i in 1:nrows){
  nmd$Sum[i]=sum(nmd[i,2:ncol])
}
ranked_nmd=nmd[order(-nmd$Sum),]
clusterdfplot(ranked_nmd[,1:15],15, main="Top 15 k-mers by line")
