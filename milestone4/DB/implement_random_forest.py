import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error

def implement_random_forest(X_train, y_train, X_test, y_test, n_estimators=100, max_depth=10, min_samples_split=2, k=5):
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)
    
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42,
        n_jobs=-1  # Use all available cores
    )
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    
    # Perform cross-validation
    scores = cross_val_score(model, X_train, y_train, cv=kf, scoring='r2')
    
    # Fit final model
    model.fit(X_train, y_train)
    
    # Get predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    return scores.mean(), scores.std(), model.feature_importances_, y_pred_train, y_pred_test

def get_performance_metrics(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    return r2, mse

if __name__ == "__main__":
    X_train = pd.read_csv("../../data/2024q3/X_train.csv")
    y_train = pd.read_csv("../../data/2024q3/y_train.csv")
    X_test = pd.read_csv("../../data/2024q3/X_test.csv")
    y_test = pd.read_csv("../../data/2024q3/y_test.csv")
    
    # Optionally: select a subset of features
    feature_subset = ['MAX SHAMT','STD SHAMT','STD VALUE','MEAN VALUE','MAX VALUE','MIN VALUE']
    X_train, X_test = X_train[feature_subset], X_test[feature_subset]
    
    mean_score, std_score, feature_importances, y_pred_train, y_pred_test = implement_random_forest(
        X_train, y_train, X_test, y_test, 
        n_estimators=100,
        max_depth=10, 
        min_samples_split=2, 
        k=5
    )
    
    print(f"Mean R^2 score: {mean_score}")
    print(f"Standard deviation of R^2 score: {std_score}")
    
    # Evaluate metrics
    train_r2, train_mse = get_performance_metrics(y_train, y_pred_train)
    test_r2, test_mse = get_performance_metrics(y_test, y_pred_test)
    
    print(f"Training R^2 score: {train_r2}")
    print(f"Training MSE: {train_mse}")
    print(f"Test R^2 score: {test_r2}")
    print(f"Test MSE: {test_mse}")
    
    # Print feature importances
    feature_names = X_train.columns
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importances
    }).sort_values('importance', ascending=False)
    print("\nFeature Importances:")
    print(importance_df)