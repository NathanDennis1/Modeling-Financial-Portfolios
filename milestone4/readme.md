# Milestone 4 readme

## XGBoost Description

XGBoost stands for Extreme Gradient Boosting which is a scalable, distributed gradient boosting decision tree machine learning method. First, we learned gradient boosting is a boosting method which additvely generates 'weak learners' and utilizes a gradient descent algorithm to create an ensemble, stronger model. Targeted outcomes for each subsequent tree in this method is based on the errors/residuals of the previous model, creating a new model based on the residuals of the previous model.

Now, XGBoost is similar to Gradient Boosting in the sense that it builds an ensemble of weak learners sequentially, where the subsequent models would correct the errors of the previous model by minimizing a loss function using a gradient descent like procedure. XGBoost has several notable improvements and changes compared to this method however:

### Regularization/Shrinkage

XGBoost incorporates both L1 (Lasso) and L2 (Ridge) Regularization terms in the objective/loss function. Similar to other regression techniques such as linear or logistic regression, these regularization parameters help to prevent overfitting by penalizing overly complex models and makes the final ensemble more robust. The L1 regularization can push leaf weights to 0, similar to lasso in linear regression and can remove features from the model entirely which can be seen as feature selection. In our case, the loss function is the mean squared error.

$$
\begin{align*}
L = \sum_{i=1}^N L(y_i, \hat{y_i}) + \lambda \sum_{t=1}^T w_t^2 + \alpha \sum_{t=1}^T |w_T|
\end{align*}
$$

Where $\lambda$ is the L2 regularization parameter and $\alpha$ is the L1 regularization parameter. The first Loss is summed over all training examples, the MSE. The second and third sum represent the regularization term applied to the weights of the leaves in the decision trees, summing over all the T trees in the ensemble.

### Parallelization

XGBoost can parallelize the tree building process, but this doesn't mean training multiple trees in parallel but rather finding the optimal splits within each tree. It parallelizes the computation of splits for each node in the tree, when we find the best possible split at each node we have to evaluate every feature at different feature thresholds to find which to split on. Instead of checking ont at a time, XGBoost performs this in parallel, meaning it evaluates multiple splits at the same time which speeds up the process of finding the best split.

### Tree Pruning

XGBoost uses depth-first growth rather than the traditional level order we discussed in class regarding single decision trees. The tree is growth depth-first, it makes all of the splits along one path for a branch first before moving to the next branch. This helps to improve the computation performance of the algorithm.

### Feature Importance

We can easily extract the feature importance from XGBoost models, in contrast to Gradient Boosting models which require external steps.

### References

https://www.analyticsvidhya.com/blog/2018/09/an-end-to-end-guide-to-understand-the-math-behind-xgboost/

https://medium.com/@dakshrathi/regularization-in-xgboost-with-9-hyperparameters-ce521784dca7#:~:text=Regularization%20in%20XGBoost%20helps%20mitigate,tailored%20to%20the%20training%20data.

https://gabrieltseng.github.io/posts/2018-02-25-XGB/

### The Algorithm

XGBoost starts with a simple model, such as a stump or depth 2 decision tree. It adds decision trees sequentially in the same manner as Gradient Boosting, where the second tree will try to correct the mistakes from the initial model's residuals. Trees are added sequentially to the model, every tree trying to correct the residuals of the previous model. As stated previously, XGBoost uses a depth-first tree growth growing one branch at a time before the next node, but if the trees are stumps it is essentially the same as level-order growth.

The objective function in XGBoost is made up of 2 parts, a loss function to measure how far off the model's predictions are from the true values, and the regularizaiton term to prevent the model from overfitting by penalizing overly complex trees. The XGBoost algorithm wants to minimize this objective function in training the model, it attempts to both reduce the loss in the current tree by improving predictions on the training data and keep model complexity low. At each split, the algorithm will look for the best feature to split and minimize the objective function, considering both reduction in the loss function and complexity penalty.

The XGBoost algorithm uses a depth-first tree growth, exploring one branch fully before moving to the next. The algorithm stops once some maximum number of estimators/trees is reached, in which case the final model is created based on the combination of all previous models.