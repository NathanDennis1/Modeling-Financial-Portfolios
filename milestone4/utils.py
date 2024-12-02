import pandas as pd
import numpy as np
import csv

def get_stats(df_info):
    s = df_info.groupby(by="ACCESSION_NUMBER")['VALUE'].mean()
    s = s.rename("MEAN VALUE")
    df_stats = s.to_frame()
    df_stats['MIN VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].min()
    df_stats['MAX VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].max()
    df_stats['STD VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].std()
    df_stats['25% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.25)
    df_stats['50% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.50)
    df_stats['75% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.75)
    df_stats['10% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.10)
    df_stats['90% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.90)
    df_stats['99% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.99)
    df_stats['01% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.01)
    
    df_stats['MEAN SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].mean()
    df_stats['MIN SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].min()
    df_stats['MAX SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].max()
    df_stats['STD SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].std()
    df_stats['25% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.25)
    df_stats['50% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.50)
    df_stats['75% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.75)
    df_stats['10% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.10)
    df_stats['90% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.90)
    df_stats['99% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.99)
    df_stats['01% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.01)
    df_stats = df_stats.reset_index()
    return df_stats

def UnitedStatesIndicator(x):
        state_df = pd.read_csv("../../data/state_list.csv")
        state_set = set(list(state_df['Abbreviation']))
        return (x in state_set) # check if the location is in the US based on the state abbreviation
    
def get_country_state(x):
    # Initialize an empty dictionary
    state_dict = {}
    # Open the CSV file
    with open('../../data/state_country_abbreviations.csv', mode='r') as file:
        reader = csv.reader(file,skipinitialspace = True)
        # Iterate through the rows in the file
        for row in reader:
            # Assign the first column as the key and the second column as the value
            state_dict[row[0]] = row[1]
    try: return state_dict[x]
    except KeyError: return np.nan
    
main_path = "../../data/2024q3"

features = [
        'TABLEENTRYTOTAL',
        'TABLEVALUETOTAL',
        'MIN VALUE',
        'MAX VALUE',
        'MEAN VALUE',
        'STD VALUE',
        '25% VALUE',
        '50% VALUE',
        '75% VALUE',
        '01% VALUE',
        '99% VALUE',
        '10% VALUE',
        '90% VALUE',
        'MIN SHAMT',
        'MAX SHAMT',
        'MEAN SHAMT',
        'STD SHAMT',
        '25% SHAMT',
        '50% SHAMT',
        '75% SHAMT',
        '01% SHAMT',
        '99% SHAMT',
        '10% SHAMT',
        '90% SHAMT',
    ]

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.model_selection import train_test_split

def assemble_dataset():
    df_cover = pd.read_csv(f'{main_path}/COVERPAGE.tsv', sep='\t')
    df_info = pd.read_csv(f'{main_path}/INFOTABLE.tsv', sep='\t')
    df_summary = pd.read_csv(f'{main_path}/SUMMARYPAGE.tsv', sep='\t')
    
    df_info = df_info[df_info['SSHPRNAMTTYPE'] == 'SH']
    df_info = df_info[df_info['ACCESSION_NUMBER'] != '0001104659-24-089646']
    df_info = df_info[df_info['ACCESSION_NUMBER'] != '0000894189-24-004736']
    df_info['SSHPRNAMT'] = df_info['SSHPRNAMT'].astype(float)
    
    df_investor = df_cover.merge(df_summary, how='inner', on='ACCESSION_NUMBER')
    
    df_investor['US_Indicator'] = df_investor['FILINGMANAGER_STATEORCOUNTRY'].apply(UnitedStatesIndicator)
    
    df_investor['State_Country_Full'] = df_investor['FILINGMANAGER_STATEORCOUNTRY'].apply(get_country_state)
    # df_us = df_investor[df_investor['US_Indicator'] == True]
    df_us = df_investor
        
    # New dataframe for summary stats
    df_stats = get_stats(df_info)
    
    df_state_gdp = pd.read_csv("../../data/state-gdp.csv")
    df_us2 = df_us
    df_us2 = df_us2.merge(right=df_stats, how='left',on='ACCESSION_NUMBER')
    df_us2['FILINGMANAGER_CITY'] = df_us2['FILINGMANAGER_CITY'].str.lower()
    
    from constants import features
    
    feature_list = features + ['OTHERINCLUDEDMANAGERSCOUNT', 'US_Indicator']
    df_star = df_us2[feature_list]  
    return df_star

def process_dataset(X_train, X_test, y_train, y_test):
    numeric_features = [
        'TABLEENTRYTOTAL','MIN VALUE', 'MAX VALUE', 'MEAN VALUE',
        'STD VALUE', '25% VALUE', '50% VALUE', '75% VALUE', '01% VALUE', '99% VALUE',
        '10% VALUE', '90% VALUE', 'MIN SHAMT', 'MAX SHAMT', 'MEAN SHAMT', 'STD SHAMT',
        '25% SHAMT', '50% SHAMT', '75% SHAMT', '01% SHAMT', '99% SHAMT', '10% SHAMT',
        '90% SHAMT', 'OTHERINCLUDEDMANAGERSCOUNT'
    ]
    
    boolean_features = ['US_Indicator']
    
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
    X_train = pd.concat([X_train_num, X_train[boolean_features]], axis=1)
    X_test = pd.concat([X_test_num, X_test[boolean_features]], axis=1)
    
    # Fill in 0 values with 0.0001 to avoid log(0) error
    y_train = y_train.replace(0, 0.0001)
    y_test = y_test.replace(0, 0.0001)
    
    # Take the log of the target variable
    y_train = np.log(y_train)
    y_test = np.log(y_test)
    
    return X_train, X_test, y_train, y_test

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error

def implement_decision_tree(X_train, y_train, X_test, y_test, max_depth=10, min_samples_split=2, k=5):
    model = DecisionTreeRegressor(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42
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

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn.metrics import r2_score, mean_squared_error

def implement_linear_regression(X_train, y_train,X_test, y_test, k=5):
    model = LinearRegression()
    kf = KFold(n_splits=k, shuffle=True, random_state=0)
    
    # Perform cross-validation
    scores = cross_val_score(model, X_train, y_train, cv=kf, scoring='r2')
    
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    return scores.mean(), scores.std(), model.coef_, model.intercept_, y_pred_train, y_pred_test

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

