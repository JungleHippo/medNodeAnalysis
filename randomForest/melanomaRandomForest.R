# Importing the libraries
library(caTools)
library(caret)
###########
# Reading the data
###########
cancerCdfRed <- read.table('./Cancer_cdfRed.csv', 
                           header = T, sep = ',')
healthyCdfRed <- read.table('./Healthy_cdfRed.csv', 
                            header = F, sep = ',')
cancerCdfBlue <- read.table('./Cancer_cdfBlue.csv', 
                            header = F, sep = ',')

healthyCdfBlue <- read.table('./Healthy_cdfBlue.csv', 
                             header = F, sep = ',')

cancerCdfGreen <- read.table('./Cancer_cdfGreen.csv', 
                             header = F, sep = ',')

healthyCdfGreen <- read.table('./Healthy_cdfGreen.csv', 
                              header = F, sep = ',')
#################
x <- c(0:255) # X axis (intensities from 0 to 255)
# Creating the matrixes to be used for the ML model
healthyPar <- matrix(0,nrow = 7, ncol = (ncol(healthyCdfRed)), byrow = T)
rownames(healthyPar) <- c('AsympR', 'Sum_sq_resR', 'AsympG', 'Sum_sq_resG', 'AsympB', 'Sum_sq_resB', 'disease')
colnames(healthyPar) <- colnames(healthyCdfRed)

cancerPar <- matrix(1,nrow = 7, ncol = (ncol(cancerCdfRed)), byrow = T)
rownames(cancerPar) <- c('AsympR', 'Sum_sq_resR', 'AsympG', 'Sum_sq_resG', 'AsympB', 'Sum_sq_resB', 'disease')
colnames(cancerPar) <- colnames(cancerCdfRed)
###########

# Calculating the Lorenzian fit and assigning the results to the par matrixes (sum of squared residuals and asymptote)
for (i in 1:100) {
  yR <- healthyCdfRed[,i]
  yB <- healthyCdfBlue[,i]
  yG <- healthyCdfGreen[,i]
  fitR <- nls(yR ~ SSlogis(x, Asym, xmid, scal), data = data.frame(x,yR))
  fitB <- nls(yB ~ SSlogis(x, Asym, xmid, scal), data = data.frame(x,yB))
  fitG <- nls(yG ~ SSlogis(x, Asym, xmid, scal), data = data.frame(x,yG))
  AsympR <- fitR$m$getPars()[1]
  AsympB <- fitB$m$getPars()[1]
  AsympG <- fitG$m$getPars()[1]
  healthyPar[1,i] <- AsympR
  healthyPar[2,i] <- sum(resid(fitR)^2)
  healthyPar[3,i] <- AsympG
  healthyPar[4,i] <- sum(resid(fitG)^2)
  healthyPar[5,i] <- AsympB
  healthyPar[6,i] <- sum(resid(fitB)^2)
}
for (i in 1:70) {
  yR <- cancerCdfRed[,i]
  yB <- cancerCdfBlue[,i]
  yG <- cancerCdfGreen[,i]
  fitR <- nls(yR ~ SSlogis(x, Asym, xmid, scal), data = data.frame(x,yR))
  fitB <- nls(yB ~ SSlogis(x, Asym, xmid, scal), data = data.frame(x,yB))
  fitG <- nls(yG ~ SSlogis(x, Asym, xmid, scal), data = data.frame(x,yG))
  AsympR <- fitR$m$getPars()[1]
  AsympB <- fitB$m$getPars()[1]
  AsympG <- fitG$m$getPars()[1]
  cancerPar[1,i] <- AsympR
  cancerPar[2,i] <- sum(resid(fitR)^2)
  cancerPar[3,i] <- AsympG
  cancerPar[4,i] <- sum(resid(fitG)^2)
  cancerPar[5,i] <- AsympB
  cancerPar[6,i] <- sum(resid(fitB)^2)
}
dataset = as.data.frame(rbind(t(cancerPar)[1:70,], t(healthyPar)[1:100,]))
dataset$disease[dataset$disease==1] = 'Yes'
dataset$disease[dataset$disease==0] = 'No'
dataset$disease = factor(dataset$disease, levels = c('No','Yes'))

split = sample.split(dataset$disease, SplitRatio = .8)
training = subset(dataset, split==T)
test = subset(dataset, split == F)

ctrl <- trainControl(method = 'repeatedcv', number = 10, repeats = 6, summaryFunction = multiClassSummary, classProbs = T)

rfModel <- train(disease ~ ., 
                    data = training, method = 'rf',
                    trControl = ctrl,
                    preProc = c('center', 'scale'),
                    metric = 'Accuracy',
                    tuneGrid = expand.grid(.mtry=seq(1:5)))
pred <- predict(rfModel,newdata = test)
cm <- confusionMatrix(pred, test$disease)
print(cm) 
print(rfModel)
