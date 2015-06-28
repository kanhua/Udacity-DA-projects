
data.path="/Users/kanhua/Documents/Big Data/KDDCup2015Data/train/"

#Load the data frame "log_events" into the memory
load(paste(data.path,"log_train.RData",sep=""))
#log_events<-read.csv(paste(data.path,"log_train.csv",sep=""))

course_obj<-read.csv("/Users/kanhua/Documents/Big Data/KDDCup2015Data/object.csv")

#head(log_events)
names(log_events)

#head(course_obj)
names(course_obj)

new_frame=merge(log_events,course_obj,by.x="object",by.y="module_id")
new_frame2=merge(log_events,course_obj,by.x="object",by.y="children")
