##### IMPLEMENTATION OF RANDOM FOREST ALGORITHM #####
##### DATASET: GERMAN CREDIT DATA #####

#Call libraries
#Classification and regression based on a forest of trees using random
library(randomForest)
library(caret)
library(rpart)

# Load the dataset and explore
data = read.csv(choose.files(),header= T)
#Showing first 6 rows
head(data)
#showing the structure of the data
str(data)


#Converting categorical value to factor
data$Creditability=as.factor(data$Creditability)

#Data Visualization
#Histogram Showing the Age Against the number of people
hist(data$Age..years., main = "Histogram of AGE", xlab = "Age", ylab = "Number of People", col = "green", border = "black" )
#Histgram Showing the purpose against the total purchased items
hist(data$Purpose, main = "Histogram of Purchase",
     xlab = "Purpose", ylab = "Total Purchase Of particular Item", col = "Blue", border = "black" )
#the correlation between the Age and Purpose 
cor(data$Age..years,data$Purpose )


# Split into Train and Validation sets

set.seed(123)
# Training Set : Validation Set = 70 : 30 random
train <- sample(nrow(data), 0.7*nrow(data), replace = FALSE)
TrainSet <- data[train,]
TestSet <- data[-train,]
# Showing the dimentions of the training set 
dim(TrainSet)
# Create a Random Forest model
model.Rf <- randomForest(Creditability ~ ., data = TrainSet)
#showing the model
model.Rf

# A plot represents the number of trees against the error rate 
plot(model.Rf)


# Making Predictions Using the random forest model
prediction <- predict(model.Rf, TestSet)

# Checking classification accuracy using the confusion Matrix
confmtrx =table(prediction,TestSet$Creditability)
confmtrx
confusionMatrix(confmtrx)

#other ways of checking accuracy
mean(prediction == TestSet$Creditability)   
p = (sum(diag(confmtrx)))/sum(confmtrx)
p
# comparing the Random Forest model with Decision Tree model
# building Decision tree model
model_dt = rpart(Creditability ~ ., data = TrainSet, method = "class")
model_dt
# Making Predictions Using the Decision tree model
dt.prediction = predict(model_dt,TestSet, type= 'class')
# Checking classification accuracy using the confusion Matrix
confmtrx2 =table(TestSet$Creditability,dt.prediction)
confmtrx2
confusionMatrix(confmtrx2)
mean(dt.prediction == TestSet$Creditability)  
# Comparing Decision tree model to Random Forest model
comparison = matrix(c(mean(dt.prediction == TestSet$Creditability),mean(prediction == TestSet$Creditability)))
rownames(comparison)=c('Decision tree model','Random Forest model')
comparison
#Random forest has higher Accuracy
