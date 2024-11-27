import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score

def implement_model(X, y, k=5):
    model = LinearRegression()
    kf = KFold(n_splits=k, shuffle=True, random_state=0)
    
    # Perform cross-validation
    scores = cross_val_score(model, X, y, cv=kf, scoring='r2')
    
    return scores.mean(), scores.std()

# Example usage
if __name__ == "__main__":
    df = pd.read_csv("../../data/2024_Q2/encoded_data.csv")
    features = [x for x in df.columns.values if x != 'TABLEVALUETOTAL']
    X = pd.read_csv("../../data/2024_Q2/X_train.csv")
    y = pd.read_csv("../../data/2024_Q2/y_train.csv")
    
    mean_score, std_score = implement_model(X, y, k=5)
    print(f"Mean R^2 score: {mean_score}")
    print(f"Standard deviation of R^2 score: {std_score}")