import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.model_selection import train_test_split

def process_dataset(X_train, X_test, y_train, y_test):
    numeric_features = [
        'TABLEENTRYTOTAL','MIN VALUE', 'MAX VALUE', 'MEAN VALUE',
        'STD VALUE', '25% VALUE', '50% VALUE', '75% VALUE', '01% VALUE', '99% VALUE',
        '10% VALUE', '90% VALUE', 'MIN SHAMT', 'MAX SHAMT', 'MEAN SHAMT', 'STD SHAMT',
        '25% SHAMT', '50% SHAMT', '75% SHAMT', '01% SHAMT', '99% SHAMT', '10% SHAMT',
        '90% SHAMT', 'OTHERINCLUDEDMANAGERSCOUNT', 'Month', 'Year'
    ]
    
    boolean_features = ['US_Indicator']
    
    # date_features = ['REPORTDATE']
    
    
    # Define the pipeline for numeric features
    numeric_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('log_transform', FunctionTransformer(np.log1p, validate=False)),
        ('scaler', StandardScaler())
    ])
    
    # Apply the pipeline to the numeric features
    X_train_num = numeric_pipeline.fit_transform(X_train[numeric_features])
    X_test_num = numeric_pipeline.transform(X_test[numeric_features])
    
    # Convert the result back to DataFrame
    X_train_num = pd.DataFrame(X_train_num, columns=numeric_features, index=X_train.index)
    X_test_num = pd.DataFrame(X_test_num, columns=numeric_features, index=X_test.index)
    
    # Handle boolean columns
    for col in boolean_features:
        mode_value = X_train[col].mode()[0]
        X_train[col] = X_train[col].fillna(mode_value)
        X_test[col] = X_test[col].fillna(mode_value)

    # Combine all features
    X_train = pd.concat(
        [X_train_num, X_train[boolean_features]], axis=1)
    X_test = pd.concat(
        [X_test_num, X_test[boolean_features]], axis=1)
    
    # Fill in 0 values with 0.0001 to avoid log(0) error
    # Impute Nan values with 0.0001
    y_train = y_train.fillna(0.0001)
    y_test = y_test.fillna(0.0001)
    
    y_train = y_train.replace(0, 0.0001)
    y_test = y_test.replace(0, 0.0001)
    
    # Take the log of the target variable
    y_train = np.log(y_train)
    y_test = np.log(y_test)
    
    return X_train, X_test, y_train, y_test
#
if __name__ == "__main__":
    df = pd.read_csv("../../data/timeseries_encoded_data.csv")
    features = [x for x in df.columns.values if x != 'TABLEVALUETOTAL']
    X = df[features]
    y = df['TABLEVALUETOTAL']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0, shuffle=True)

    print("Train/test split complete.")
    X_train, X_test, y_train, y_test = process_dataset(X_train, X_test, y_train, y_test)

    # Save to CSV files

    # Save to CSV files
    X.to_csv("../../data/timeseries_X.csv", index=False)
    y.to_csv("../../data/timeseries_y.csv", index=False)
    df.to_csv("../../data/timeseries_processed_data.csv", index=False)
    
    X_train.to_csv("../../data/timeseries_X_train.csv", index=False)
    X_test.to_csv("../../data/timeseries_X_test.csv", index=False)
    y_train.to_csv("../../data/timeseries_y_train.csv", index=False)
    y_test.to_csv("../../data/timeseries_y_test.csv", index=False)