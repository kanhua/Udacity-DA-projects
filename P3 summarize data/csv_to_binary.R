
data.path="/Users/kanhua/Documents/Big Data/KDDCup2015Data/train/"

#Load the data frame "log_events" into the memory

log_events<-read.csv(paste(data.path,"log_train.csv",sep=""))
save(log_events,file=paste(data.path,"log_train.RData",sep=""))
#object<-read.csv("/Users/kanhua/Documents/Big Data/KDDCup2015Data/object.csv")
