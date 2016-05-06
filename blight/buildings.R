require(ggplot2)
require(GGally)
require(scales)
require(caret)
require(randomForest)

setwd('~/projects/public_scripts/blight')
data = read.csv('building_blight_features.csv',
                  header = TRUE)
# set categorical values
data$blight = factor(data$blight)

data = na.omit(data)
summary(data)
# select the training observations
in_train = createDataPartition(y = data$blight,
                               p = 0.75, # 75% in train, 25% in test
                               list = FALSE)

train = data[in_train, ]
test = data[-in_train, ]

# drop the ids and coordinates
train$Address = NULL
test$Address = NULL
train$Latitude = NULL
test$Latitude = NULL
train$Longitude = NULL
test$Longitude = NULL

tree_model = train(factor(blight) ~., 
                   method = 'rpart',
                   data = train)
print(tree_model)
print(tree_model$finalModel)
plot(varImp(tree_model))

# plot the tree!
plot(tree_model$finalModel)
text(tree_model$finalModel, use.n = TRUE, all = TRUE, cex = 0.60)


# test the predictions
tree_predictions = predict(tree_model, newdata = test)
confusionMatrix(tree_predictions, test$blight)

bagged_model = train(blight ~.,
                     method = 'treebag',
                     data = train)
print(bagged_model)
print(bagged_model$finalModel)

bagged_predictions = predict(bagged_model, test)
confusionMatrix(bagged_predictions, test$blight)

boost_model = train(blight ~.,
                    method = 'gbm',
                    data = train,
                    verbose = FALSE)
print(boost_model)
plot(boost_model)
summary(boost_model$finalModel)

# predict
boost_predictions = predict(boost_model, test)
confusionMatrix(boost_predictions, test$blight)

rf_model = train(blight ~.,
                 data = train,
                 method = 'rf',
                 prox = TRUE,
                 verbose = TRUE)

print(rf_model)
summary(rf_model)
plot(rf_model)
plot(rf_model$finalModel)

# pull a tree out of the forest
getTree(rf_model$finalModel, k = 5)

# predict
rf_predictions = predict(rf_model, test)
confusionMatrix(rf_predictions, test$blight)

# compare
results = resamples(list(tree_model = tree_model, 
                         bagged_model = bagged_model,
                         boost_model = boost_model))

# compare accuracy and kappa
summary(results)

# plot results
dotplot(results)