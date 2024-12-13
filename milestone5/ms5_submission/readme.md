# Milestone 4 readme

- David Bombara, Aditya Saxena, and Nathan Dennis
- AC 209A Class Project

## Project Structure

- `data/` contains the data files used in the project
- `main_notebook/` contains the notebook used to generate the results.
- `utils.py` contains the utility functions used in the notebook.
- `MS4_Combined.ipynb` contains the Jupyter notebook.
- `requirements.txt` contains the required packages to run the notebook.

## Project Description

In this project, we study the Form 13F datasets. The Form 13F data sets are derived from EDGAR filings, a system managed by the U.S. Securities and Exchange Commission (SEC). Form 13F filings are required by institutional managers with over $100 million in assets under management to disclose their quarterly holdings. The goal of these filings is to provide transparency in the activities and holdings of large managers in the financial markets. The data sets are extracted from XML files in EDGAR Form 13F and made available as tab-delimited text files on a quarterly basis. These files are generated from structured filings by institutional managers and are compiled into seven specific tables within each quarterly data set.

The data includes up to seven different tables, each representing different aspects of the filing information:

1. COVERPAGE: Provides cover page information like the filing manager's name, address, and report type. Key details include the report calendar quarter, amendment information, confidentiality status, and filing manager details.
2. SUMMARYPAGE: Offers a high-level summary of the filing, including counts of other included managers, the table entry total, and the total value of holdings. It also notes if certain information was confidentially omitted.
3. INFOTABLE: The primary data table containing detailed information about each holding, such as issuer name, class title, market value, share quantity, and voting authority. Key fields include ACCESSION_NUMBER, INFOTABLE_SK, and several columns providing identifiers for the financial instruments.

## XGBoost Description

Because XGBoost was not covered during class, below we present a brief overview of the algorithm and how it differs from other boosting algorithms we covered in class.

XGBoost stands for Extreme Gradient Boosting which is a scalable, distributed gradient boosting decision tree machine learning method. First, we learned gradient boosting is a boosting method which additvely generates 'weak learners' and utilizes a gradient descent algorithm to create an ensemble, stronger model. Targeted outcomes for each subsequent tree in this method is based on the errors/residuals of the previous model, creating a new model based on the residuals of the previous model.

Now, XGBoost is similar to Gradient Boosting in the sense that it builds an ensemble of weak learners sequentially, where the subsequent models would correct the errors of the previous model by minimizing a loss function using a gradient descent like procedure. XGBoost has several notable improvements and changes compared to this method however:

### Regularization/Shrinkage

XGBoost incorporates both L1 (Lasso) and L2 (Ridge) Regularization terms in the objective/loss function. Similar to other regression techniques such as linear or logistic regression, these regularization parameters help to prevent overfitting by penalizing overly complex models and makes the final ensemble more robust. The L1 regularization can push leaf weights to 0, similar to lasso in linear regression and can remove features from the model entirely which can be seen as feature selection. L2 can help reduce impact of large weights. In our case, the loss function is the mean squared error and is defined below:

$$
\begin{align*}
L = \sum_{i=1}^N L(y_i, \hat{y_i}) + \lambda \sum_{t=1}^T w_t^2 + \alpha \sum_{t=1}^T |w_T|
\end{align*}
$$

Where $\lambda$ is the L2 regularization parameter and $\alpha$ is the L1 regularization parameter, then $w_t$ the weight of the leaf node of the t-th tree. Also, $N$ is the number of training samples, $T$ the number of total trees in the ensemble and $L = \sum_{i=1}^N L(y_i, \hat{y_i})$ is the original MSE loss function. The first Loss is summed over all training examples, the MSE. The second and third sum represent the regularization term applied to the weights of the leaves in the decision trees, summing over all the T trees in the ensemble. This is the major difference we found compared to other boosting algorithms we covered in the class, these regularization terms.

### Parallelization

XGBoost can parallelize the tree building process, but this doesn't mean training multiple trees in parallel but rather finding the optimal splits within each tree. It parallelizes the computation of splits for each node in the tree. When we find the best possible split at each node in other methods, we have to evaluate every feature at different feature thresholds to find which to split on. Instead of checking one at a time, XGBoost performs this in parallel, meaning it evaluates multiple splits at the same time across different features which speeds up the process of finding the best split and the overall training process.

### Tree Pruning

XGBoost uses depth-first growth rather than the traditional level order growth we discussed in class regarding single decision trees. The tree is growth depth-first, it makes all of the splits along one path for a branch first before moving to the next branch. Basically, the algorithm fully expands one branch before moving onto the next unlike level-order which processes each level (depth) sequentially. This helps to improve the computation performance of the algorithm

### References

https://www.analyticsvidhya.com/blog/2018/09/an-end-to-end-guide-to-understand-the-math-behind-xgboost/

https://medium.com/@dakshrathi/regularization-in-xgboost-with-9-hyperparameters-ce521784dca7#:~:text=Regularization%20in%20XGBoost%20helps%20mitigate,tailored%20to%20the%20training%20data.

https://gabrieltseng.github.io/posts/2018-02-25-XGB/

### The Algorithm

XGBoost starts with a simple model, such as a stump or depth 2 decision tree. It adds decision trees sequentially in the same manner as Gradient Boosting, where the second tree will try to correct the mistakes from the initial model's residuals. Trees are added sequentially to the model, every tree trying to correct the residuals of the previous model. As stated previously, XGBoost uses a depth-first tree growth growing one branch at a time before the next node, but if the trees are stumps it is essentially the same as level-order growth.

The objective function in XGBoost is made up of 2 parts, a loss function to measure how far off the model's predictions are from the true values, and the regularizaiton term to prevent the model from overfitting by penalizing overly complex trees. The XGBoost algorithm wants to minimize this objective function in training the model, it attempts to both reduce the loss in the current tree by improving predictions on the training data and keep model complexity low. At each split, the algorithm will look for the best feature to split and minimize the objective function, considering both reduction in the loss function and complexity penalty.

The XGBoost algorithm uses a depth-first tree growth, exploring one branch fully before moving to the next. The algorithm stops once some maximum number of estimators/trees is reached, in which case the final model is created based on the combination of all previous models.