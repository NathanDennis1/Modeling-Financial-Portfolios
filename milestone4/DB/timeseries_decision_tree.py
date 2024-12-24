import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score, mean_squared_error

def implement_timeseries_tree(X_train, y_train, X_test, y_test, max_depth=10, min_samples_split=2, n_splits=5):
    model = DecisionTreeRegressor(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42
    )
    
    # Use TimeSeriesSplit instead of KFold
    tscv = TimeSeriesSplit(n_splits=n_splits)
    
    # Perform time series cross-validation
    scores = []
    for train_idx, val_idx in tscv.split(X_train):
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
        
        model.fit(X_tr, y_tr)
        score = r2_score(y_val, model.predict(X_val))
        scores.append(score)
    
    # Fit final model
    model.fit(X_train, y_train)
    
    # Get predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    return np.mean(scores), np.std(scores), model.feature_importances_, y_pred_train, y_pred_test

def get_performance_metrics(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    return r2, mse

if __name__ == "__main__":
    # Load data
    X_train = pd.read_csv("../../data/timeseries_X_train.csv")
    y_train = pd.read_csv("../../data/timeseries_y_train.csv")
    X_test = pd.read_csv("../../data/timeseries_X_test.csv")
    y_test = pd.read_csv("../../data/timeseries_y_test.csv")
    # Create time features
    
    feature_subset = ['MAX SHAMT', 'STD SHAMT', 'STD VALUE', 'MEAN VALUE', 'MAX VALUE', 'MIN VALUE',
                     'Year', 'Month']
    
    X_train = X_train[feature_subset]
    X_test = X_test[feature_subset]
    
    mean_score, std_score, feature_importances, y_pred_train, y_pred_test = implement_timeseries_tree(
        X_train, y_train, X_test, y_test, max_depth=20, min_samples_split=2, n_splits=10
    )
    
    # Calculate performance metrics
    train_r2, train_mse = get_performance_metrics(y_train, y_pred_train)
    test_r2, test_mse = get_performance_metrics(y_test, y_pred_test)
    
    print("\nCross-validation Results:")
    print(f"Mean R^2 score: {mean_score:.4f}")
    print(f"Standard deviation of R^2 score: {std_score:.4f}")
    
    print("\nTraining Performance:")
    print(f"R^2 score: {train_r2:.4f}")
    print(f"MSE: {train_mse:.4f}")
    print(f"RMSE: {np.sqrt(train_mse):.4f}")
    
    print("\nTesting Performance:")
    print(f"R^2 score: {test_r2:.4f}")
    print(f"MSE: {test_mse:.4f}")
    print(f"RMSE: {np.sqrt(test_mse):.4f}")
    
    # Print feature importances
    importance_df = pd.DataFrame({
        'feature': feature_subset,
        'importance': feature_importances
    }).sort_values('importance', ascending=False)
    print("\nFeature Importances:")
    print(importance_df)